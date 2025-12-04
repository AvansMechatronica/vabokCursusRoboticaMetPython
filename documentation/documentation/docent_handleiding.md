# Docent Handleiding

## Installatie van software op de pico-robot
Volg de stappen in de les "Software installeren op de pico-robot" om Thonny en de benodigde firmware te installeren.

**Stap 1.1:** Verbind de Raspberry Pi Pico
- Houd de **BOOTSEL** knop op de Pico ingedrukt (klein wit knopje)
- Sluit de USB-kabel aan op de Pico (terwijl je de knop ingedrukt houdt!)
- Sluit de andere kant van de USB-kabel aan op je computer
- Laat de BOOTSEL knop los
- De Pico verschijnt als een USB-schijf (zoals een USB-stick)

**Stap 1.2:** Installeer MicroPython firmware
- In Thonny: klik rechtsonder op **"Python"**
- Kies **"MicroPython (Raspberry Pi Pico)"**
- Er verschijnt een venster: klik op **"Install or update firmware"**
- Selecteer de juiste COM-poort (meestal iets als COM3 of COM4)
- Klik op **"Install"**
- Wacht tot het klaar is (dit duurt ongeveer 10 seconden)

**Stap 3.1:** Kopieer de bibliotheek bestanden
- Open de Windows Verkenner
- Ga naar de map: `Pico-Robot/Appendix/Library/`
- Je het volgend bestand:
  - `pico_car.py`


**Stap 3.2:** Upload naar de Pico
- Zorg dat de Pico is verbonden met Thonny
- In Thonny: klik op **"View"** → **"Files"**
- Je ziet nu twee panelen: je computer (boven) en Raspberry Pi Pico (onder)
- Sleep `pico_car.py` naar het Raspberry Pi Pico paneel
- Het bestand wordt geüpload naar de Pico