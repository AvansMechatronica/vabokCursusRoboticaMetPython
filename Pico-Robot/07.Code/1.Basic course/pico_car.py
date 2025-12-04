"""
================================================================================
PICO CAR BIBLIOTHEEK - Volledige robotbesturing voor Raspberry Pi Pico
================================================================================

Deze bibliotheek bevat alle benodigde klassen en functies om de Pico Robot
aan te sturen. Het ondersteunt:

KLASSEN:
    - pico_car:      Hoofdklasse voor motor- en servobesturing
    - ws2812b:       RGB LED strip besturing (NeoPixels)
    - ultrasonic:    Ultrasone afstandssensor
    - SSD1306:       OLED display basisklasse
    - SSD1306_I2C:   OLED display via I2C communicatie
    - ir:            Infrarood ontvanger voor afstandsbediening
    - ds:            DS18B20 temperatuursensor (OneWire)

HARDWARE PINOUT:
    Motoren:
        - Linker motor A: GPIO 12 (L_A)
        - Linker motor B: GPIO 13 (L_B)
        - Rechter motor A: GPIO 10 (R_A)
        - Rechter motor B: GPIO 11 (R_B)
    
    Servo's:
        - Servo 1: GPIO 18
        - Servo 2: GPIO 19
        - Servo 3: GPIO 20
        - Servo 4: GPIO 21
    
    Sensoren en overig:
        - Ultrasone Trigger: GPIO 0
        - Ultrasone Echo: GPIO 1
        - WS2812B LEDs: GPIO 6
        - Infrarood ontvanger: GPIO 7
        - I2C SDA (OLED): GPIO 14
        - I2C SCL (OLED): GPIO 15

AUTEUR: Pico Robot Team
VERSIE: 1.0
DATUM: 2024
================================================================================
"""

import array, time
import machine, onewire
from machine import Pin, PWM
from onewire import OneWire
import rp2
import framebuf

# ============================================================================
# PWM PINNEN CONFIGURATIE
# ============================================================================

# Servo PWM pinnen (S1 t/m S4) - voor robotarm of andere servo toepassingen
S1 = PWM(Pin(18))  # Servo aansluiting 1
S2 = PWM(Pin(19))  # Servo aansluiting 2
S3 = PWM(Pin(20))  # Servo aansluiting 3
S4 = PWM(Pin(21))  # Servo aansluiting 4

# Motor PWM pinnen voor H-brug motor driver
# Rechter motor (R) en Linker motor (L)
# A = vooruit, B = achteruit
R_B = PWM(Pin(11))  # Rechter motor achteruit
R_A = PWM(Pin(10))  # Rechter motor vooruit
L_B = PWM(Pin(13))  # Linker motor achteruit
L_A = PWM(Pin(12))  # Linker motor vooruit

# ============================================================================
# SSD1306 OLED DISPLAY REGISTER DEFINITIES
# ============================================================================
# ============================================================================
# SSD1306 OLED DISPLAY REGISTER DEFINITIES
# ============================================================================
# Deze constanten definiëren de commando's voor het OLED scherm

SET_CONTRAST        = 0x81  # Stel contrast/helderheid in
SET_ENTIRE_ON       = 0xa4  # Zet hele display aan
SET_NORM_INV        = 0xa6  # Normaal of geïnverteerde weergave
SET_DISP            = 0xae  # Display aan/uit
SET_MEM_ADDR        = 0x20  # Geheugen adresseringsmodus
SET_COL_ADDR        = 0x21  # Kolom adres instellen
SET_PAGE_ADDR       = 0x22  # Pagina adres instellen
SET_DISP_START_LINE = 0x40  # Display startlijn
SET_SEG_REMAP       = 0xa0  # Segment remapping
SET_MUX_RATIO       = 0xa8  # Multiplex ratio
SET_COM_OUT_DIR     = 0xc0  # COM output scan richting
SET_DISP_OFFSET     = 0xd3  # Display offset
SET_COM_PIN_CFG     = 0xda  # COM pinnen hardware configuratie
SET_DISP_CLK_DIV    = 0xd5  # Display klok deler
SET_PRECHARGE       = 0xd9  # Pre-charge periode
SET_VCOM_DESEL      = 0xdb  # VCOM deselect niveau
SET_CHARGE_PUMP     = 0x8d  # Charge pump instelling
# ============================================================================
# WS2812B LED STRIP DRIVER (PIO Assembly)
# ============================================================================
# Deze functie gebruikt de Programmable I/O (PIO) van de RP2040 chip
# om de WS2812B RGB LED strip aan te sturen met nauwkeurige timing

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    """
    PIO state machine programma voor WS2812B LEDs
    
    Timing parameters voor WS2812B protocol:
    - T1 = HIGH tijd voor een '1' bit (800ns)
    - T2 = LOW tijd voor een '1' bit (450ns)  
    - T3 = HIGH tijd voor een '0' bit (400ns)
    
    De state machine stuurt 24-bit RGB data naar de LED strip
    """
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()

# ============================================================================
# PICO_CAR KLASSE - Hoofdbesturing voor robot
# ============================================================================

class pico_car:
    """
    Hoofdklasse voor het aansturen van de Pico Robot.
    
    Deze klasse regelt:
    - Motor besturing (vooruit, achteruit, draaien, stoppen)
    - Servo motor controle (180°, 270°, en 360° servo's)
    
    GEBRUIK:
        Motor = pico_car()
        Motor.Car_Run(255, 255)    # Rij vooruit op volle snelheid
        Motor.Car_Stop()           # Stop de robot
    """
    
    def __init__(self):
        """
        Initialiseer de robot door PWM frequenties in te stellen.
        
        Servo's krijgen 100 Hz (standaard voor servo's)
        Motoren krijgen 1000 Hz (voor soepele motor besturing)
        """
        # Stel servo PWM frequenties in (100 Hz = 10ms periode)
        S1.freq(100)
        S2.freq(100)
        S3.freq(100)
        S4.freq(100)
        
        # Stel motor PWM frequenties in (1000 Hz voor soepel draaien)
        R_B.freq(1000)
        R_A.freq(1000)
        L_B.freq(1000)
        L_A.freq(1000)
        
    def Car_Run(self, speed1, speed2):
        """
        Laat de robot vooruit rijden.
        
        Parameters:
            speed1 (int): Snelheid linker motor (0-255)
            speed2 (int): Snelheid rechter motor (0-255)
        
        Werking:
            - Zet beide motoren in voorwaartse richting
            - L_B en R_A krijgen PWM signaal voor vooruit
            - L_A en R_B staan uit
        
        Voorbeeld:
            Motor.Car_Run(255, 255)  # Volle snelheid vooruit
            Motor.Car_Run(150, 150)  # Halve snelheid vooruit
            Motor.Car_Run(200, 150)  # Vooruit met bocht naar rechts
        """
        # Converteer snelheid van 0-255 naar 0-65535 (16-bit PWM)
        speed1 = speed1 * 257  # Linker motor snelheid
        speed2 = speed2 * 257  # Rechter motor snelheid
        
        # Rechter motor vooruit
        R_B.duty_u16(0)        # Achteruit uit
        R_A.duty_u16(speed2)   # Vooruit aan met snelheid
        
        # Linker motor vooruit
        L_B.duty_u16(speed1)   # Vooruit aan met snelheid
        L_A.duty_u16(0)        # Achteruit uit
        
    def Car_Stop(self):
        """
        Stop de robot volledig.
        
        Zet alle motor PWM signalen op 0, waardoor beide motoren stoppen.
        Gebruik deze functie altijd aan het einde van een beweging om
        de robot gecontroleerd te laten stoppen.
        
        Voorbeeld:
            Motor.Car_Run(255, 255)
            time.sleep(2)
            Motor.Car_Stop()  # Stop na 2 seconden
        """
        R_B.duty_u16(0)  # Rechter motor achteruit uit
        R_A.duty_u16(0)  # Rechter motor vooruit uit
        L_B.duty_u16(0)  # Linker motor vooruit uit
        L_A.duty_u16(0)  # Linker motor achteruit uit
    
    def Car_Back(self, speed1, speed2):
        """
        Laat de robot achteruit rijden.
        
        Parameters:
            speed1 (int): Snelheid linker motor (0-255)
            speed2 (int): Snelheid rechter motor (0-255)
        
        Werking:
            - Zet beide motoren in achterwaartse richting
            - R_B en L_A krijgen PWM signaal voor achteruit
            - R_A en L_B staan uit
        
        Voorbeeld:
            Motor.Car_Back(200, 200)  # Achteruit rijden
        """
        # Converteer snelheid van 0-255 naar 0-65535 (16-bit PWM)
        speed1 = speed1 * 257
        speed2 = speed2 * 257
        
        # Rechter motor achteruit
        R_B.duty_u16(speed2)   # Achteruit aan met snelheid
        R_A.duty_u16(0)        # Vooruit uit
        
        # Linker motor achteruit
        L_B.duty_u16(0)        # Vooruit uit
        L_A.duty_u16(speed1)   # Achteruit aan met snelheid
        
    def Car_Left(self, speed1, speed2):
        """
        Laat de robot op de plaats naar links draaien.
        
        Parameters:
            speed1 (int): Snelheid linker motor (0-255)
            speed2 (int): Snelheid rechter motor (0-255)
        
        Werking:
            - Linker motor draait achteruit
            - Rechter motor draait vooruit
            - Robot draait linksom op zijn as
        
        Voorbeeld:
            Motor.Car_Left(150, 150)  # Draai links met gemiddelde snelheid
        """
        # Converteer snelheid van 0-255 naar 0-65535 (16-bit PWM)
        speed1 = speed1 * 257
        speed2 = speed2 * 257
        
        # Rechter motor vooruit (voor linkse draai)
        R_B.duty_u16(0)
        R_A.duty_u16(speed2)
        
        # Linker motor achteruit (voor linkse draai)
        L_B.duty_u16(0)
        L_A.duty_u16(speed1)
        
    def Car_Right(self, speed1, speed2):
        """
        Laat de robot op de plaats naar rechts draaien.
        
        Parameters:
            speed1 (int): Snelheid linker motor (0-255)
            speed2 (int): Snelheid rechter motor (0-255)
        
        Werking:
            - Linker motor draait vooruit
            - Rechter motor draait achteruit
            - Robot draait rechtsom op zijn as
        
        Voorbeeld:
            Motor.Car_Right(150, 150)  # Draai rechts met gemiddelde snelheid
        """
        # Converteer snelheid van 0-255 naar 0-65535 (16-bit PWM)
        speed1 = speed1 * 257
        speed2 = speed2 * 257
        
        # Rechter motor achteruit (voor rechtse draai)
        R_B.duty_u16(speed2)
        R_A.duty_u16(0)
        
        # Linker motor vooruit (voor rechtse draai)
        L_B.duty_u16(speed1)
        L_A.duty_u16(0)
        
    def servo180(self, num, angle):
        """
        Bestuur een 180 graden servo motor.
        
        Parameters:
            num (int): Servo nummer (1-4)
            angle (int): Gewenste hoek (0-180 graden)
        
        Een 180° servo kan draaien van 0 tot 180 graden.
        0° = helemaal links, 90° = midden, 180° = helemaal rechts
        
        De hoek wordt omgezet naar een PWM waarde:
        - Formule: PWM = hoek * 72.2222 + 3535
        - Dit geeft pulsbreedte van ~1ms (0°) tot ~2ms (180°)
        
        Voorbeeld:
            Motor.servo180(1, 90)   # Zet servo 1 naar middenpositie
            Motor.servo180(2, 0)    # Zet servo 2 naar uiterst links
            Motor.servo180(3, 180)  # Zet servo 3 naar uiterst rechts
        """
        # Bereken PWM waarde uit hoek (0-180 graden)
        angle = angle * 72.2222 + 3535
        
        # Selecteer de juiste servo en stel PWM in
        if num == 1:
            S1.duty_u16(int(angle))
        elif num == 2:
            S2.duty_u16(int(angle))
        elif num == 3:
            S3.duty_u16(int(angle))
        elif num == 4:
            S4.duty_u16(int(angle))
            
    def servo270(self, num, angle):
        """
        Bestuur een 270 graden servo motor.
        
        Parameters:
            num (int): Servo nummer (1-4)
            angle (int): Gewenste hoek (0-270 graden)
        
        Een 270° servo heeft een groter bereik dan een standaard servo.
        0° = uiterst links, 135° = midden, 270° = uiterst rechts
        
        De hoek wordt omgezet naar een PWM waarde:
        - Formule: PWM = hoek * 48.1481 + 3535
        
        Voorbeeld:
            Motor.servo270(1, 135)  # Zet servo 1 naar middenpositie
            Motor.servo270(2, 0)    # Zet servo 2 naar uiterst links
        """
        # Bereken PWM waarde uit hoek (0-270 graden)
        angle = angle * 48.1481 + 3535
        
        # Selecteer de juiste servo en stel PWM in
        if num == 1:
            S1.duty_u16(int(angle))
        elif num == 2:
            S2.duty_u16(int(angle))
        elif num == 3:
            S3.duty_u16(int(angle))
        elif num == 4:
            S4.duty_u16(int(angle))
            
       
    def servo360(self, num, angle):
        """
        Bestuur een 360 graden (continu rotatie) servo motor.
        
        Parameters:
            num (int): Servo nummer (1-4)
            angle (int): Rotatie snelheid/richting (0-360)
        
        Een 360° servo is eigenlijk een continue rotatie motor:
        - 0° = volle snelheid achteruit
        - 180° = stop
        - 360° = volle snelheid vooruit
        
        De waarde wordt omgezet naar een PWM waarde:
        - Formule: PWM = waarde * 36.1111 + 3535
        
        Voorbeeld:
            Motor.servo360(1, 180)  # Stop servo 1
            Motor.servo360(2, 270)  # Draai servo 2 vooruit
            Motor.servo360(3, 90)   # Draai servo 3 achteruit
        """
        # Bereken PWM waarde uit rotatie waarde (0-360)
        angle = angle * 36.1111 + 3535
        
        # Selecteer de juiste servo en stel PWM in
        if num == 1:
            S1.duty_u16(int(angle))
        elif num == 2:
            S2.duty_u16(int(angle))
        elif num == 3:
            S3.duty_u16(int(angle))
        elif num == 4:
            S4.duty_u16(int(angle))

# ============================================================================
# WS2812B LED STRIP KLASSE
# ============================================================================

class ws2812b:
    """
    Klasse voor het aansturen van WS2812B RGB LED strips (NeoPixels).
    
    Deze LEDs zijn adresseerbaar, wat betekent dat elke LED individueel
    een kleur kan krijgen. Ze worden vaak gebruikt voor:
    - Status indicatie (rood = stop, groen = go)
    - Lichteffecten (regenboog, vloeiende kleuren)
    - Visuele feedback
    
    GEBRUIK:
        pixels = ws2812b(8, 0)           # 8 LEDs, state machine 0
        pixels.set_pixel(0, 255, 0, 0)   # LED 0 rood
        pixels.set_pixel(1, 0, 255, 0)   # LED 1 groen
        pixels.show()                     # Toon de kleuren
    """
    
    def __init__(self, num_leds, state_machine, delay=0.001):
        """
        Initialiseer de WS2812B LED strip.
        
        Parameters:
            num_leds (int): Aantal LEDs in de strip
            state_machine (int): PIO state machine nummer (0-7)
            delay (float): Vertragingstijd na update (seconden)
        
        De delay is de reset tijd voor de LED strip. Een korte pauze
        is nodig om de LED strip terug te zetten naar de initiële staat.
        Als je veel processing doet tussen updates, kun je delay=0 gebruiken.
        """
        # Maak een array voor pixel kleuren (32-bit per pixel: RGB)
        self.pixels = array.array("I", [0 for _ in range(num_leds)])
        
        # Start de PIO state machine voor WS2812 protocol
        self.sm = rp2.StateMachine(state_machine, ws2812, freq=8000000, sideset_base=Pin(6))
        self.sm.active(1)  # Activeer de state machine
        
        self.num_leds = num_leds
        self.delay = delay
        self.brightnessvalue = 255  # Maximale helderheid (0-255)

    # ========================================================================
    # HELDERHEID CONTROLE
    # ========================================================================
    
    def brightness(self, brightness=None):
        """
        Stel de helderheid van alle LEDs in of vraag huidige helderheid op.
        
        Parameters:
            brightness (int, optional): Helderheid (1-255)
                - None: Geef huidige helderheid terug
                - 1-255: Stel nieuwe helderheid in
        
        Returns:
            int: Huidige helderheid (als geen parameter wordt gegeven)
        
        Voorbeeld:
            pixels.brightness(100)     # Zet helderheid op 100
            current = pixels.brightness()  # Lees huidige helderheid
        """
        if brightness == None:
            return self.brightnessvalue
        else:
            # Beperk helderheid tussen 1 en 255
            if (brightness < 1):
                brightness = 1
            if (brightness > 255):
                brightness = 255
            self.brightnessvalue = brightness

    # ========================================================================
    # LED PIXEL FUNCTIES
    # ========================================================================
      
    def set_pixel_line_gradient(self, pixel1, pixel2, left_red, left_green, left_blue, right_red, right_green, right_blue):
        """
        Maak een vloeiend kleurverloop tussen twee pixels.
        
        Parameters:
            pixel1 (int): Start pixel nummer
            pixel2 (int): Eind pixel nummer
            left_red, left_green, left_blue (int): Start kleur RGB (0-255)
            right_red, right_green, right_blue (int): Eind kleur RGB (0-255)
        
        Voorbeeld:
            # Maak gradient van rood (pixel 0) naar blauw (pixel 7)
            pixels.set_pixel_line_gradient(0, 7, 255, 0, 0, 0, 0, 255)
        """
        if pixel2 - pixel1 == 0: 
            return
    
        right_pixel = max(pixel1, pixel2)
        left_pixel = min(pixel1, pixel2)
        
        # Bereken kleur voor elke pixel in het verloop
        for i in range(right_pixel - left_pixel + 1):
            fraction = i / (right_pixel - left_pixel)
            red = round((right_red - left_red) * fraction + left_red)
            green = round((right_green - left_green) * fraction + left_green)
            blue = round((right_blue - left_blue) * fraction + left_blue)
            
            self.set_pixel(left_pixel + i, red, green, blue)
    
    def set_pixel_line(self, pixel1, pixel2, red, green, blue):
        """
        Zet een reeks pixels naar dezelfde kleur.
        
        Parameters:
            pixel1 (int): Start pixel
            pixel2 (int): Eind pixel (inclusief)
            red, green, blue (int): RGB kleurwaarden (0-255)
        
        Voorbeeld:
            pixels.set_pixel_line(0, 3, 255, 0, 0)  # Pixels 0-3 rood
        """
        for i in range(pixel1, pixel2 + 1):
            self.set_pixel(i, red, green, blue)

    def set_pixel(self, pixel_num, red, green, blue):
        """
        Zet een individuele pixel naar een specifieke kleur.
        
        Parameters:
            pixel_num (int): Pixel nummer (0 tot num_leds-1)
            red, green, blue (int): RGB kleurwaarden (0-255)
        
        De kleuren worden automatisch aangepast op basis van de
        ingestelde helderheid.
        
        Voorbeeld:
            pixels.set_pixel(0, 255, 0, 0)    # Pixel 0 rood
            pixels.set_pixel(1, 0, 255, 0)    # Pixel 1 groen
            pixels.set_pixel(2, 0, 0, 255)    # Pixel 2 blauw
        """
        # Pas kleurwaarden aan met helderheid
        blue = round(blue * (self.brightness() / 255))
        red = round(red * (self.brightness() / 255))
        green = round(green * (self.brightness() / 255))

        # Sla kleur op in 32-bit formaat: [0][G][R][B]
        self.pixels[pixel_num] = blue | red << 8 | green << 16
    
    # ========================================================================
    # ROTATIE FUNCTIES
    # ========================================================================
    
    def rotate_left(self, num_of_pixels):
        """
        Roteer alle pixels een aantal posities naar links.
        
        Parameters:
            num_of_pixels (int): Aantal posities om te roteren (standaard 1)
        
        Dit creëert een "lopend licht" effect waarbij de kleuren
        naar links verschuiven.
        
        Voorbeeld:
            pixels.rotate_left(1)  # Roteer 1 positie naar links
            pixels.rotate_left(2)  # Roteer 2 posities naar links
        """
        if num_of_pixels == None:
            num_of_pixels = 1
        # Verplaats pixels: pak eerste n pixels en zet ze achteraan
        self.pixels = self.pixels[num_of_pixels:] + self.pixels[:num_of_pixels]

    def rotate_right(self, num_of_pixels):
        """
        Roteer alle pixels een aantal posities naar rechts.
        
        Parameters:
            num_of_pixels (int): Aantal posities om te roteren (standaard 1)
        
        Dit creëert een "lopend licht" effect waarbij de kleuren
        naar rechts verschuiven.
        
        Voorbeeld:
            pixels.rotate_right(1)  # Roteer 1 positie naar rechts
        """
        if num_of_pixels == None:
            num_of_pixels = 1
        # Verplaats pixels naar rechts door negatieve rotatie naar links
        num_of_pixels = -1 * num_of_pixels
        self.pixels = self.pixels[num_of_pixels:] + self.pixels[:num_of_pixels]

    def show(self):
        """
        Stuur de pixel data naar de LED strip.
        
        Deze functie moet aangeroepen worden NA het instellen van de
        pixel kleuren met set_pixel() of andere functies. Pas dan worden
        de kleuren zichtbaar op de LEDs.
        
        Voorbeeld:
            pixels.set_pixel(0, 255, 0, 0)  # Stel kleur in
            pixels.set_pixel(1, 0, 255, 0)  # Stel kleur in
            pixels.show()                    # Toon de kleuren!
        """
        for i in range(self.num_leds):
            self.sm.put(self.pixels[i], 8)  # Stuur 32-bit kleurdata naar PIO
        time.sleep(self.delay)  # Wacht even voor reset timing
            
    def fill(self, red, green, blue):
        """
        Zet alle pixels naar dezelfde kleur.
        
        Parameters:
            red, green, blue (int): RGB kleurwaarden (0-255)
        
        Handig om alle LEDs tegelijk uit te zetten (0,0,0) of
        om een uniforme kleur in te stellen.
        
        Voorbeeld:
            pixels.fill(255, 0, 0)  # Alle LEDs rood
            pixels.fill(0, 0, 0)    # Alle LEDs uit
            pixels.show()            # Vergeet niet te tonen!
        """
        for i in range(self.num_leds):
            self.set_pixel(i, red, green, blue)
        time.sleep(self.delay)


# ============================================================================
# ULTRASONIC AFSTANDSSENSOR KLASSE
# ============================================================================

class ultrasonic():
    """
    Klasse voor het uitlezen van de HC-SR04 ultrasone afstandssensor.
    
    Deze sensor werkt met geluidsgolven:
    1. Stuur een korte puls uit via de Trigger pin
    2. Wacht tot de Echo pin hoog wordt (echo ontvangen)
    3. Meet hoe lang de Echo pin hoog blijft
    4. Bereken afstand: tijd * geluidssnelheid / 2
    
    Bereik: 2cm tot 400cm
    Nauwkeurigheid: ±3mm
    
    GEBRUIK:
        sensor = ultrasonic()
        afstand = sensor.Distance_accurate()  # In centimeters
        print("Afstand:", afstand, "cm")
    """
    
    def __init__(self):
        """
        Initialiseer de ultrasone sensor.
        
        Pin configuratie:
            - Trigger: GPIO 0 (output) - stuurt ultrasone puls uit
            - Echo: GPIO 1 (input) - ontvangt echo terug
        """
        self.Trig = Pin(0, Pin.OUT)  # Trigger pin voor uitzenden
        self.Echo = Pin(1, Pin.IN)   # Echo pin voor ontvangen
            
    def Distance(self):
        """
        Voer een enkele afstandsmeting uit.
        
        Returns:
            float: Afstand in centimeters (of -1 bij fout)
        
        Werking:
            1. Trigger pin 10µs hoog (ultrasone puls uitgezonden)
            2. Wacht tot Echo pin hoog wordt
            3. Tel hoe lang Echo pin hoog blijft
            4. Bereken afstand uit tijd
        
        Let op: Deze functie geeft soms onbetrouwbare metingen.
        Gebruik bij voorkeur Distance_accurate() voor betere resultaten.
        """
        # Stuur trigger puls (10µs hoog)
        self.Trig.value(0)
        time.sleep(0.000002)  # 2µs laag
        self.Trig.value(1)
        time.sleep(0.000015)  # 15µs hoog (trigger puls)
        self.Trig.value(0)
        
        # Wacht tot echo start
        t2 = 0
        while not self.Echo.value():
            t1 = 0
        t1 = 0
        
        # Tel hoe lang echo hoog is
        while self.Echo.value():
            t2 += 1

        time.sleep(0.001)  # Korte pauze tussen metingen
        
        # Bereken afstand: tijd * snelheidsconversie / 10
        # Factor 2.0192 is gecalibreerd voor deze sensor
        return ((t2 - t1) * 2.0192 / 10)

    def Distance_accurate(self):
        """
        Voer een nauwkeurige afstandsmeting uit door meerdere metingen.
        
        Returns:
            int: Gemiddelde afstand in centimeters
        
        Werking:
            - Voer 5 metingen uit
            - Filter onbetrouwbare waarden (>500cm of 0cm)
            - Neem gemiddelde van middelste 3 waarden
            - Dit vermindert ruis en geeft stabielere metingen
        
        Dit is de aanbevolen functie voor betrouwbare afstandsmetingen.
        
        Voorbeeld:
            sensor = ultrasonic()
            afstand = sensor.Distance_accurate()
            if afstand < 20:
                print("Obstakel dichtbij!")
        """
        num = 0
        ultrasonic = []
        
        # Verzamel 5 metingen
        while num < 5:
            distance = self.Distance()
            
            # Filter foutieve metingen
            while int(distance) == -1:
                distance = self.Distance()
                return int(999)  # Foutcode
                
            while (int(distance) >= 500 or int(distance) == 0):
                distance = self.Distance()
                return int(999)  # Foutcode voor buiten bereik
                
            # Voeg goede meting toe aan lijst
            ultrasonic.append(distance)
            num = num + 1
            time.sleep(0.01)  # Korte pauze tussen metingen
        
        # Bereken gemiddelde van middelste 3 metingen (filter uitschieters)
        distance = (ultrasonic[1] + ultrasonic[2] + ultrasonic[3]) / 3
        return int(distance)


# ============================================================================
# SSD1306 OLED DISPLAY BASISKLASSE
# ============================================================================

class SSD1306:
    """
    Basisklasse voor SSD1306 OLED displays.
    
    Het SSD1306 is een populaire OLED display controller die wordt
    gebruikt in kleine monochrome displays (meestal 128x64 of 128x32).
    
    Deze klasse wordt niet direct gebruikt, maar dient als basis voor:
    - SSD1306_I2C (communicatie via I2C)
    - SSD1306_SPI (communicatie via SPI)
    """
    
    def __init__(self, width, height, external_vcc):
        """
        Initialiseer het OLED display.
        
        Parameters:
            width (int): Breedte in pixels (meestal 128)
            height (int): Hoogte in pixels (32 of 64)
            external_vcc (bool): True als externe voeding wordt gebruikt
        """
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height
        # De subklasse moet self.framebuf initialiseren
        self.poweron()
        self.init_display()

    def init_display(self):
        for cmd in (
            SET_DISP | 0x00, # off
            # address setting
            SET_MEM_ADDR, 0x00, # horizontal
            # resolution and layout
            SET_DISP_START_LINE | 0x00,
            SET_SEG_REMAP | 0x01, # column addr 127 mapped to SEG0
            SET_MUX_RATIO, self.height - 1,
            SET_COM_OUT_DIR | 0x08, # scan from COM[N] to COM0
            SET_DISP_OFFSET, 0x00,
            SET_COM_PIN_CFG, 0x02 if self.height == 32 else 0x12,
            # timing and driving scheme
            SET_DISP_CLK_DIV, 0x80,
            SET_PRECHARGE, 0x22 if self.external_vcc else 0xf1,
            SET_VCOM_DESEL, 0x30, # 0.83*Vcc
            # display
            SET_CONTRAST, 0xff, # maximum
            SET_ENTIRE_ON, # output follows RAM contents
            SET_NORM_INV, # not inverted
            # charge pump
            SET_CHARGE_PUMP, 0x10 if self.external_vcc else 0x14,
            SET_DISP | 0x01): # on
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def poweroff(self):
        self.write_cmd(SET_DISP | 0x00)

    def contrast(self, contrast):
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(SET_NORM_INV | (invert & 1))

    def show(self):
        x0 = 0
        x1 = self.width - 1
        if self.width == 64:
            # displays with width of 64 pixels are shifted by 32
            x0 += 32
            x1 += 32
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(x0)
        self.write_cmd(x1)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_framebuf()

    def fill(self, col):
        self.framebuf.fill(col)

    def pixel(self, x, y, col):
        self.framebuf.pixel(x, y, col)

    def scroll(self, dx, dy):
        self.framebuf.scroll(dx, dy)

    def text(self, string, x, y, col=1):
        self.framebuf.text(string, x, y, col)


class SSD1306_I2C(SSD1306):
    def __init__(self, width, height, i2c, addr=0x3c, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        # Add an extra byte to the data buffer to hold an I2C data/command byte
        # to use hardware-compatible I2C transactions.  A memoryview of the
        # buffer is used to mask this byte from the framebuffer operations
        # (without a major memory hit as memoryview doesn't copy to a separate
        # buffer).
        self.buffer = bytearray(((height // 8) * width) + 1)
        self.buffer[0] = 0x40  # Set first byte of data buffer to Co=0, D/C=1
        self.framebuf = framebuf.FrameBuffer1(memoryview(self.buffer)[1:], width, height)
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.temp[0] = 0x80 # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_framebuf(self):
        # Blast out the frame buffer using a single I2C transaction to support
        # hardware I2C interfaces.
        self.i2c.writeto(self.addr, self.buffer)

    def poweron(self):
        pass


class ir():
    def __init__(self):
        self.Pin = Pin(7)
        self.Pin.value(1)
        self.ir_repeat_cnt = 0
        self.irdata = 0xfe
            
    def Getir(self):
        if self.Pin.value() == 0:
            
            self.ir_repeat_cnt = 0
            count = 0
            while self.Pin.value() == 0:
                count += 1
                time.sleep(0.00003)

            count = 0
            while self.Pin.value() == 1 and count < 160:
                count += 1
                time.sleep(0.00003)
            #print("")
            idx = 0
            cnt = 0
            data = [0,0,0,0]
            for i in range(0,32):
                count = 0
                while self.Pin.value() == 0 and count < 30:
                    count += 1
                    time.sleep(0.00003)

                count = 0
                while self.Pin.value() == 1 and count < 80:
                    count += 1
                    time.sleep(0.00003)

                if count > 35:
                    data[idx] |= 1<<cnt
                if cnt == 7:
                    cnt = 0
                    idx += 1
                else:
                    cnt += 1
            
            if data[0]+data[1] == 0xFF and data[2]+data[3] == 0xFF:
                self.irdata = data[2]
        else:
            if self.ir_repeat_cnt > 110: 
                self.ir_repeat_cnt = 0
                self.irdata = 0xfe
            else:
                time.sleep(0.001)
                self.ir_repeat_cnt += 1
        if self.irdata != None:
            if self.irdata != 254:
                return self.irdata

class ds:
    def __init__(self, unit='c', resolution=12):
        self.pin=7
        self.no_addr=0
        self.addr=self.getaddr()
        self.unit=unit
        self.res=resolution

    def getaddr(self):
        ow=OneWire(Pin(self.pin))
        a=ow.scan()
        for i in a:
            self.no_addr+=1
        return a
        
    def read(self):
        if self.no_addr==0:
            print ("no sensors detected")
        if self.no_addr>=1:
            temp_array=[]
            #print ('number of sensors: ',self.no_addr)
            for i in range(1,self.no_addr+1):
                temp_array.append(self._request(self.addr[i-1]))
                return temp_array       
        
    def _request(self, addr):
        self._res(addr)
        ow=OneWire(Pin(self.pin))
        ow.reset()
        ow.select_rom(addr)
        ow.writebyte(0x44) #command to take reading
        if self.res==12: #the resolution determines the amount of time needed
            time.sleep_ms(1000)
        if self.res==11:
            time.sleep_ms(400)
        if self.res==10:
            time.sleep_ms(200)
        if self.res==9:
            time.sleep_ms(100)
        ow.reset() #reset required for data
        ow.select_rom(addr)
        ow.writebyte(0xBE) #command to send temperature data
        #all nine bytes must be read
        LSB=ow.readbyte() #least significant byte
        MSB=ow.readbyte() #most significant byte
        ow.readbyte()
        ow.readbyte()
        ow.readbyte() #this is the configuration byte for resolution
        ow.readbyte()
        ow.readbyte()
        ow.readbyte()
        ow.readbyte()
        ow.reset() #reset at end of data transmission
        #convert response to binary, format the binary string, and perform math
        d_LSB=float(0)
        d_MSB=float(0)
        count=0
        b=bin(LSB)
        b2=bin(MSB)
        b3=""
        l=10-len(b2)
        for i in range(l):
            if len(b2)<10:
                b3+="0"
        b2=b3+b2
        b4=""
        l=10-len(b)
        for i in range(l):
            if len(b)<10:
                b4+="0"
        b5=b4+b
        for i in b5:
            if count == 2:
                if i=='1':
                    d_LSB+=2**3
            if count == 3:
                if i=='1':
                    d_LSB+=2**2
            if count == 4:
                if i=='1':
                    d_LSB+=2**1
            if count == 5:
                if i=='1':
                    d_LSB+=2**0
            if count == 6:
                if i=='1':
                    d_LSB+=2**-1
            if count == 7:
                if i=='1':
                    d_LSB+=2**-2
            if count == 8:
                if i=='1':
                    d_LSB+=2**-3
            if count == 9:
                if i=='1':
                    d_LSB+=2**-4
            count+=1
        count=0
        sign=1
        for i in b2:
            if count == 6:
                if i=='1':
                    sign=-1
            if count == 7:
                if i=='1':
                    d_MSB+=2**6
            if count == 8:
                if i=='1':
                    d_MSB+=2**5
            if count == 9:
                if i=='1':
                    d_MSB+=2**4
            count+=1
        temp=(d_LSB+d_MSB)*sign
        '''
        if self.unit=='c'or self.unit=='C':
            print("TEMP is: "+str(temp)+" degrees C")
        if self.unit=='f'or self.unit=='F':
            temp=(temp*9/5)+32
            print("TEMP F is: "+str(temp))
        '''
        return temp

    def _res(self,addr):
        ow=OneWire(Pin(self.pin))
        ow.reset()
        ow.select_rom(addr)
        ow.writebyte(0x4E)
        if self.res==12:
            ow.writebyte(0x7F)
            ow.writebyte(0x7F)
            ow.writebyte(0x7F)
            #print ("12 bit mode")
        if self.res==11:
            ow.writebyte(0x5F)
            ow.writebyte(0x5F)
            ow.writebyte(0x5F)
            #print ("11 bit mode")
        if self.res==10:
            ow.writebyte(0x3F)
            ow.writebyte(0x3F)
            ow.writebyte(0x3F)
            #print ("10 bit mode")
        if self.res==9:
            ow.writebyte(0x1F)
            ow.writebyte(0x1F)
            ow.writebyte(0x1F)
            #print ("9 bit mode")
        ow.reset()  


