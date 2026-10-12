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

## Materialen
Voor de course zijn de volgende materialen (per student) nodig:
- Pico-robot, zie [Yahboom](https://category.yahboom.net/products/pico-robot?srsltid=AU7gw4WrzJ70YM7uN15P4GCEEBnzdfTh9Mp6qkQ_cbC0b-OCeWlQe8UG)
- Computer/laptop met volgende software geïnstalleerd:
  - [Thonny IDE](https://thonny.org/)
  - Webbrowser voor de documentatie en online bronnen
    - [Deze course documentatie](https://avansmechatronica.github.io/vabokCursusRoboticaMetPython/)
    - [Online Python](https://www.online-python.com/)
- Reserve batterijen ([link](https://www.123accu.nl/DR-INR18650-18650-Li-ion-batterij-3-6-V-2850-mAh-8-4-A-123accu-huismerk-i49322.html))
- Batterijenlader ([link](https://www.123accu.nl/Nitecore-i4-Oplader-voor-Li-ion-LiFePO4-Ni-Mh-Batterijen-i31489.html)), 1 lader per 2 studenten
- USB-adapter ([bijvoorbeeld link](https://www.123accu.nl/Xtorm-Next-Gen-Wall-Charger-USB-C-45-W-i59620.html))
- micro USB-A kabel ([link](https://www.123accu.nl/search/?search=micro+USB-A+kabel))
- 3d-prints van werktuigen voor de Pico-robot, zie course documentatie
- Toetsing
  - Magazijn circuits
  - Robot-werktuigen
