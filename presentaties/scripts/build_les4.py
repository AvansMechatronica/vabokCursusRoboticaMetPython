"""Bouwt de presentatie voor les 4: Programmeren van actoren.
Gebruik: python build_les4.py <repo-root> <uitvoer.pptx> <screenshot-website.png>"""
import os, sys
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "helpers.py"), encoding="utf-8").read())

IMG = ROOT + "/documentation/images/"
IMG_SITE = sys.argv[3]

# ---------------------------------------------------------------- titel + planning
titel("4: Programmeren van actoren",
      "Welkom. Vandaag laat je de robot dingen doen: rijden, licht geven, tekst tonen en geluid maken.\n"
      "Zoals altijd: korte uitleg op het juiste moment, de rest werk je zelfstandig uit met de online handleiding.")

agenda([
    ("12:30  ", "Introductie en terugblik"),
    ("12:45  ", "Motoren (opdracht 1 en 2)"),
    ("13:15  ", "LED"),
    ("13:35  ", "OLED-display"),
    ("14:00  ", "Pauze"),
    ("14:15  ", "Buzzer en functies"),
    ("14:50  ", "Alles combineren + NeoPixels (next level)"),
    ("15:30  ", "Afsluiting en vooruitblik"),
], "De tijden zijn richtlijnen. Wie sneller is, gaat door; NeoPixels is voor wie de rest af heeft.")

# ---------------------------------------------------------------- terugblik
s = new(L_TITLE_ONLY, "Opwarmer: wat doet de robot?",
        "Terugblik op les 3 (±3 min). Eerst voorspellen, dan pas vertellen.\n"
        "Antwoorden: 1) 2 seconden een bocht naar rechts (links sneller), daarna stop.\n"
        "2) Vier keer vooruit + draaien: een vierkant (als de draaitijd klopt).\n"
        "3) Hij stopt nooit: Car_Stop() ontbreekt. Noodstop = schakelaar op OFF.")
qs = ["Motor.Car_Run(200, 100)\ntime.sleep(2)\nMotor.Car_Stop()",
      "for i in range(4):\n    Motor.Car_Run(200, 200)\n    time.sleep(1)\n    Motor.Car_Right(200, 200)\n    time.sleep(0.5)\nMotor.Car_Stop()",
      "Motor.Car_Run(255, 255)\nprint(\"Klaar!\")"]
x = 0.8
for k, q in enumerate(qs):
    circle_num(s, x, 1.65, k + 1)
    code(s, x, 2.4, 3.75, q, size=13, h=2.4)
    box(s, x, 5.0, 3.75, 0.9, GREY)
    text(s, x + 0.2, 5.0, 3.35, 0.9, "Wat doet de robot? …", size=16, color=MUTED, italic=True, anchor=MSO_ANCHOR.MIDDLE)
    x += 4.02
strip_empty(s)

# ---------------------------------------------------------------- wat is een actor
s = new(L_TITLE_ONLY, "Wat is een actor?",
        "Kernbegrip (±3 min). Een actor zet een signaal van de computer om in een fysieke actie: beweging, licht, geluid.\n"
        "Koppel aan het schema uit les 2: invoer (sensor) → beslissen (Pico) → uitvoer (actor). Les 4 = uitvoer, les 5 = invoer.")
flow = [("Sensor", "neemt waar", "les 5", LILAC_T, NAVY),
        ("Pico", "beslist met jouw code", "les 2 en 3", BLUE_T, NAVY),
        ("Actor", "voert een actie uit", "vandaag", RED_T, RED)]
x = 0.8
for k, (h, b, l, f, c) in enumerate(flow):
    box(s, x, 1.75, 3.6, 1.9, f)
    text(s, x + 0.3, 1.9, 3.0, 0.55, h, size=24, bold=True, color=c)
    text(s, x + 0.3, 2.5, 3.0, 0.5, b, size=17)
    text(s, x + 0.3, 3.05, 3.0, 0.45, l, size=15, italic=True, color=MUTED)
    if k < 2:
        text(s, x + 3.62, 2.25, 0.5, 0.8, "→", size=36, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    x += 4.1
text(s, 0.8, 4.0, 11.8, 0.5, "Actoren op de Pico-robot", size=20, bold=True, color=NAVY)
acts = [("Motoren", "rijden en draaien"), ("LED", "aan en uit"), ("OLED-display", "tekst en pixels"),
        ("Buzzer", "piepjes en muziek"), ("NeoPixels", "8 kleuren-leds")]
x = 0.8
for k, (h, b) in enumerate(acts):
    box(s, x, 4.6, 2.2, 1.5, GREY)
    text(s, x + 0.2, 4.75, 1.9, 0.45, h, size=17, bold=True, color=RED if k < 4 else NAVY)
    text(s, x + 0.2, 5.25, 1.9, 0.7, b, size=14)
    x += 2.4
strip_empty(s)

# ---------------------------------------------------------------- leerdoelen
s = new(L_TITLE_ONLY, "Leerdoelen van vandaag",
        "Noem de vier actoren. NeoPixels is extra voor snelle studenten. Nieuw programmeerbegrip vandaag: de functie (def).")
card(s, 0.8, 1.7, 5.7, 4.4, "Je kunt…", [
    "• de motoren aansturen in een reeks bewegingen", "• een LED aan- en uitzetten",
    "• tekst tonen op het OLED-display", "• tonen en melodietjes spelen met de buzzer",
    "• actoren combineren in één programma"], fill=LILAC_T, size=19)
card(s, 6.9, 1.7, 5.7, 4.4, "Nieuw in Python", [
    [("def", {"font": "Courier New", "bold": True, "color": RED}), ("  een eigen functie maken", {})],
    [("while True:", {"font": "Courier New", "bold": True, "color": RED}), ("  blijven herhalen", {})],
    [("Pin, PWM", {"font": "Courier New", "bold": True, "color": RED}), ("  aansluitingen van de Pico", {})],
    "", "Next level: NeoPixels in alle kleuren"], fill=BLUE_T, size=19)
strip_empty(s)

website(["Open de website (link hieronder)", "Kies in het menu links Les 4",
         "Per actor: voorbeeldcode + opdracht", "Uitleg van de code via de link onder elk voorbeeld"],
        "Laat de website zien. Bij elk codevoorbeeld staat een link naar een pagina met regel-voor-regel uitleg.", IMG_SITE)

# ================================================================ DEEL 1
deel(L_DEEL_A, "Deel 1", "Motoren, LED en display",
     "Start deel 1 (12:45). Robot klaarzetten: batterijen, schakelaar, USB-kabel, Thonny verbonden.")

# ---------------------------------------------------------------- motoren
s = new(L_TITLE_ONLY, "Motoren: een reeks bewegingen",
        "Korte herhaling (±3 min). Een programma is een reeks opdrachten die van boven naar beneden wordt uitgevoerd.\n"
        "time.sleep() bepaalt hoe lang een beweging duurt. Bij opdracht 2 schrijven ze een eigen 'choreografie'.\n"
        "Veiligheid: robot op de grond of vasthouden.")
_, y2 = code(s, 0.8, 1.7, 6.2, "from pico_car import pico_car\nimport time\n\nMotor = pico_car()\n\nMotor.Car_Run(255, 255)   # vooruit\ntime.sleep(3)             # 3 seconden\nMotor.Car_Run(255, 120)   # bocht rechts\ntime.sleep(2)\nMotor.Car_Stop()", size=15)
uitleg_rijen(s, 7.3, 1.7, 5.3, [
    ("Car_Run(l, r)", "vooruit; snelheid 0–255 per motor"),
    ("Car_Back(l, r)", "achteruit"),
    ("Car_Run(255, 120)", "links sneller: bocht naar rechts"),
    ("Car_Stop()", "stoppen; ook tussendoor, met sleep"),
])
next_step(s, "opdracht 1 en 2: motoren")
strip_empty(s)

doen("Aan de slag: motoren", [
    ("1  ", "Experimenteer met snelheden en richtingen"),
    ("2  ", "3 s vooruit, 2 s bocht rechts, 3 s vooruit, 2 s stop, 5 s achteruit, stop"),
    ("Tip: ", "zet bij elke stap een # comment"),
], "Opdrachten motoren (±25 min). Robot op de grond. Wie snel klaar is: maak de route mooier of korter.",
    foot="Lesmateriaal: les 4, Motoren")

# ---------------------------------------------------------------- LED
s = new(L_TITLE_ONLY, "LED: aan en uit",
        "Just-in-time uitleg (±4 min). Een Pin is een aansluitpunt van de Pico. Pin 25 is de LED op de Pico zelf.\n"
        "value(1) = aan, value(0) = uit. while True herhaalt eindeloos; stoppen met de Stop-knop in Thonny.\n"
        "Checkvraag: 'Hoe laat je de LED sneller knipperen?'")
_, y2 = code(s, 0.8, 1.7, 6.2, "import machine\nimport time\n\nled = machine.Pin(25, machine.Pin.OUT)\n\nwhile True:\n    led.value(1)      # aan\n    time.sleep(1)\n    led.value(0)      # uit\n    time.sleep(1)", size=16)
uitleg_rijen(s, 7.3, 1.7, 5.3, [
    ("Pin(25, Pin.OUT)", "aansluiting 25 als uitgang"),
    ("led.value(1)", "stroom aan: LED brandt"),
    ("led.value(0)", "stroom uit: LED uit"),
    ("while True:", "blijf herhalen tot je op Stop drukt"),
])
next_step(s, "opdracht LED")
strip_empty(s)

doen("Aan de slag: LED", [
    ("Opdracht  ", "Breid je motorprogramma uit: LED aan als de robot rijdt, uit als hij stopt"),
    ("Extra  ", "Laat de LED knipperen terwijl de robot achteruit rijdt"),
], "Opdracht LED (±15 min). Hint: zet led.value(1) vlak voor Car_Run en led.value(0) vlak na Car_Stop.\n"
   "Knipperen tijdens rijden: een for-loop met korte sleeps terwijl de motoren draaien.",
    foot="Lesmateriaal: les 4, LED")

# ---------------------------------------------------------------- display
s = new(L_TITLE_ONLY, "OLED-display: tekst op het scherm",
        "Just-in-time uitleg (±5 min). Het scherm is 128 x 32 pixels. Positie (0, 0) is linksboven; y gaat naar beneden.\n"
        "Belangrijk: oled.text() tekent eerst in het geheugen, pas oled.show() zet het op het scherm. oled.fill(0) maakt alles zwart.\n"
        "Checkvraag: 'Waarom zie je niets als je show() vergeet?'")
# schermpje
box(s, 0.8, 1.75, 5.6, 1.6, BLACK, radius=0.04)
text(s, 1.0, 1.85, 5.2, 0.5, "Hello", size=22, color=COMMENT, font="Courier New", bold=True)
text(s, 1.0, 2.45, 5.2, 0.5, "World", size=22, color=COMMENT, font="Courier New", bold=True)
text(s, 0.8, 3.45, 5.6, 0.4, [[("(0, 0)", {"bold": True, "font": "Courier New"}), (" linksboven  ·  x → 128  ·  y ↓ 32", {})]], size=14, color=MUTED)
code(s, 0.8, 4.0, 5.6, "oled.text(\"Hello\", 0, 0)\noled.text(\"World\", 0, 10)\noled.show()\noled.fill(0)   # scherm wissen", size=15)
uitleg_rijen(s, 6.9, 1.7, 5.7, [
    ("I2C(1, scl=15, sda=14)", "de verbinding met het scherm"),
    ("SSD1306_I2C(128, 32, i2c)", "het scherm: 128 x 32 pixels"),
    ("oled.text(tekst, x, y)", "tekst tekenen op positie x, y"),
    ("oled.show()", "pas nu verschijnt het op het scherm"),
    ("oled.fill(0)", "alles wissen (zwart)"),
])
next_step(s, "opdracht display")
strip_empty(s)

doen("Aan de slag: display", [
    ("Opdracht  ", "Toon \"Pico Robot\" als de robot rijdt en \"Stopped\" als hij stopt"),
    ("Extra  ", "Laat een getal aftellen op het scherm: 3, 2, 1, start!"),
], "Opdracht display (±15 min). Veelgemaakte fout: oude tekst blijft staan. Oplossing: eerst oled.fill(0), dan text(), dan show().\n"
   "Getallen tonen: oled.text(str(i), 0, 0).",
    foot="Lesmateriaal: les 4, Display")

pauze("Pauze\n14:15 verder met deel 2",
      "Pauze (14:00–14:15). Robot uitzetten (schakelaar OFF) zodat de batterijen niet leeglopen.")

# ================================================================ DEEL 2
deel(L_DEEL_B, "Deel 2", "Buzzer, functies en alles combineren",
     "Start deel 2 (14:15). Waarschuw: met 20 piepende robots wordt het luid. Spreek af: korte tonen testen.")

# ---------------------------------------------------------------- buzzer
s = new(L_TITLE_ONLY, "Buzzer: tonen maken",
        "Just-in-time uitleg (±5 min). De frequentie (Hz) bepaalt de toonhoogte: hoger getal = hogere toon.\n"
        "duty_u16 zet het geluid aan (500) of uit (0). Vergeet je duty_u16(0), dan blijft de buzzer piepen.\n"
        "Probeer samen: 262 Hz (do) en 523 Hz (do, een octaaf hoger).")
_, y2 = code(s, 0.8, 1.7, 6.2, "from machine import Pin, PWM\nimport time\n\nBZ = PWM(Pin(22))      # buzzer op pin 22\n\nBZ.freq(1000)          # toonhoogte in Hz\nBZ.duty_u16(500)       # geluid aan\ntime.sleep(0.2)        # 0,2 seconde\nBZ.duty_u16(0)         # geluid uit!", size=15)
uitleg_rijen(s, 7.3, 1.7, 5.3, [
    ("PWM(Pin(22))", "aan/uit schakelen, heel snel"),
    ("BZ.freq(1000)", "toonhoogte: 1000 trillingen per seconde"),
    ("BZ.duty_u16(500)", "geluid aan"),
    ("BZ.duty_u16(0)", "geluid uit, anders blijft hij piepen"),
])
box(s, 0.8, y2 + 0.25, 6.2, 0.75, BLUE_T)
text(s, 1.0, y2 + 0.25, 5.8, 0.75, [[("Lage toon ", {"bold": True}), ("262 Hz    ", {"font": "Courier New"}),
                                    ("Hoge toon ", {"bold": True}), ("1047 Hz", {"font": "Courier New"})]],
     size=16, anchor=MSO_ANCHOR.MIDDLE)
next_step(s, "opdracht buzzer")
strip_empty(s)

# ---------------------------------------------------------------- functies
s = new(L_TITLE_ONLY, "Nieuw: een eigen functie met def",
        "Just-in-time uitleg (±5 min). Het muziekvoorbeeld in de handleiding gebruikt def music(). Een functie is een blokje code met een naam\n"
        "dat je zo vaak kunt aanroepen als je wilt. Net als print(), maar dan zelfgemaakt.\n"
        "Laat zien: definiëren (def) doet nog niets; pas aanroepen (piep()) voert de code uit.")
code(s, 0.8, 1.7, 6.2, "def piep():\n    BZ.freq(1000)\n    BZ.duty_u16(500)\n    time.sleep(0.2)\n    BZ.duty_u16(0)\n\n# gebruiken:\nMotor.Car_Run(200, 200)\npiep()\ntime.sleep(2)\nMotor.Car_Stop()\npiep()\npiep()", size=15)
card(s, 7.3, 1.7, 5.3, 2.0, "def  =  maken", ["Je geeft een stukje code een naam.", "Er gebeurt nog niets."],
     fill=LILAC_T, size=16)
card(s, 7.3, 3.9, 5.3, 2.0, "piep()  =  gebruiken", ["Elke keer dat je piep() schrijft,", "wordt de code uitgevoerd."],
     fill=BLUE_T, size=16)
next_step(s, "opdracht buzzer")
strip_empty(s)

doen("Aan de slag: buzzer", [
    ("1  ", "Speel het liedje uit de handleiding af (functie music)"),
    ("2  ", "Opdracht: piepje als de robot gaat rijden en als hij stopt"),
    ("Extra  ", "Maak een eigen functie, bijvoorbeeld sirene() of toeter()"),
], "Opdracht buzzer (±20 min). Laat studenten de functie piep() zelf schrijven in plaats van overtypen.",
    foot="Lesmateriaal: les 4, Buzzer")

# ---------------------------------------------------------------- neopixels
s = new(L_TITLE_ONLY, "Next level: NeoPixels",
        "Voor wie klaar is (±3 min uitleg, of laten lezen). Elke NeoPixel heeft drie kleine leds: rood, groen en blauw.\n"
        "Door ze te mengen maak je elke kleur. Gebruik kleine waarden (0–30): ze zijn erg fel en de batterij loopt snel leeg.")
code(s, 0.8, 1.7, 6.2, "from pico_car import ws2812b\nimport time\n\npixels = ws2812b(8, 0)        # 8 leds\n\npixels.fill(10, 0, 0)         # alles rood\npixels.show()\ntime.sleep(1)\n\npixels.set_pixel(0, 0, 0, 20) # led 0 blauw\npixels.show()", size=15)
kleuren = [("rood", (10, 0, 0), RGBColor(0xE0, 0x20, 0x20)), ("groen", (0, 10, 0), RGBColor(0x20, 0xA0, 0x40)),
           ("blauw", (0, 0, 10), RGBColor(0x20, 0x60, 0xE0)), ("geel", (10, 10, 0), RGBColor(0xE8, 0xC0, 0x10)),
           ("paars", (10, 0, 10), RGBColor(0x90, 0x30, 0xC0)), ("wit", (10, 10, 10), RGBColor(0xCC, 0xCC, 0xCC))]
y = 1.7
for k, (naam, rgb, col) in enumerate(kleuren):
    cx = 7.3 + (k % 2) * 2.7
    cy = 1.7 + (k // 2) * 1.05
    c = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx), Inches(cy + 0.1), Inches(0.6), Inches(0.6))
    c.fill.solid(); c.fill.fore_color.rgb = col; c.line.fill.background(); c.shadow.inherit = False
    text(s, cx + 0.75, cy + 0.05, 1.9, 0.35, naam, size=15, bold=True, color=NAVY)
    text(s, cx + 0.75, cy + 0.4, 1.9, 0.35, "%d, %d, %d" % rgb, size=14, font="Courier New")
box(s, 7.3, 4.95, 5.3, 1.15, RED_T)
text(s, 7.5, 4.95, 4.9, 1.15, [[("Tip: ", {"bold": True, "color": RED}), ("houd de waarden laag (0–30). NeoPixels zijn fel en zuigen de batterij leeg.", {})]],
     size=15, anchor=MSO_ANCHOR.MIDDLE)
strip_empty(s)

doen("Aan de slag: alles samen", [
    ("Combineer  ", "minimaal drie actoren in één programma"),
    ("Bijvoorbeeld  ", "rijden + tekst op het display + piepje bij elke bocht"),
    ("Next level  ", "NeoPixels in een kleur die past bij de richting"),
    ("Gebruik  ", "eigen functies: vooruit(), bocht(), piep()"),
], "Eindopdracht (tot ±15:30). Moedig het gebruik van functies aan: dat maakt de code overzichtelijk.\n"
   "Laat aan het eind 1 of 2 robotshows zien.",
    foot="Lesmateriaal: les 4, alle onderdelen")

# ---------------------------------------------------------------- hulpkaart
s = new(L_TITLE_ONLY, "Hulpkaart: het werkt niet, wat nu?",
        "Kan blijven staan tijdens het werken.")
kaartgrid(s, [
    ("Display blijft leeg", ["oled.show() vergeten?", "Tekst buiten beeld (y > 24)?"]),
    ("Oude tekst blijft staan", ["Eerst oled.fill(0)", "dan text() en show()"]),
    ("Buzzer blijft piepen", ["BZ.duty_u16(0) vergeten", "Noodstop: Stop in Thonny"]),
    ("Programma stopt niet", ["while True stopt nooit", "Stop-knop of Ctrl+C"]),
    ("ImportError", ["pico_car met kleine letters", "pico_car.py op de Pico?"]),
    ("Functie doet niets", ["Alleen def geschreven?", "Ook aanroepen: piep()"]),
])
strip_empty(s)

# ---------------------------------------------------------------- afsluiting
s = new(L_TITLE_ONLY, "Afsluiting: wat kun je nu?",
        "Afsluiting (15:30, ±10 min). Laat 1 of 2 robotshows zien. Schakelaar op OFF.\n"
        "Vooruitblik: in les 5 laat je de robot waarnemen met sensoren en daarop reageren.")
checklist(s, 0.8, 1.75, ["Motoren in een reeks bewegingen", "LED aan en uit", "Tekst op het OLED-display",
                         "Tonen met de buzzer", "Eigen functies met def", "Actoren combineren"])
box(s, 6.9, 1.7, 5.7, 4.5, BLUE_T)
text(s, 7.15, 1.85, 5.2, 0.5, "Volgende week: sensoren", size=20, bold=True, color=NAVY)
y = 2.55
for h_, b in [("Lichtsensoren", "hoe licht is het?"), ("Ultrasoon", "hoe ver is de muur?"),
              ("Trackingsensoren", "zie ik een zwarte lijn?")]:
    circle_num(s, 7.15, y, "→", fill=RED, d=0.45, size=14)
    text(s, 7.8, y - 0.05, 4.6, 0.55, [[(h_ + "  ", {"bold": True}), (b, {})]], size=17, anchor=MSO_ANCHOR.MIDDLE)
    y += 0.8
text(s, 7.15, 5.0, 5.2, 0.9, "Dan reageert de robot zelf op zijn omgeving: sensor → beslissen → actor.", size=16, italic=True, color=MUTED)
strip_empty(s)

afronden(OUT, "Vragen? Schakelaar op OFF en de robot veilig opbergen.")
