"""Bouwt de presentatie voor les 5: Programmeren van sensoren.
Gebruik: python build_les5.py <repo-root> <uitvoer.pptx> <screenshot-website.png>"""
import os, sys
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "helpers.py"), encoding="utf-8").read())

IMG = ROOT + "/documentation/images/"
IMG_SITE = sys.argv[3]

# ---------------------------------------------------------------- titel + planning
titel("5: Programmeren van sensoren",
      "Welkom. Vandaag leert de robot waarnemen: licht, afstand en lijnen op de grond.\n"
      "Daarna laat je hem zelf beslissen wat hij doet: sensor → beslissen → actor.")

agenda([
    ("12:30  ", "Introductie en terugblik"),
    ("12:45  ", "Lichtsensoren"),
    ("13:10  ", "Ultrasone sensor: afstand meten"),
    ("13:30  ", "Botsing vermijden (opdracht 2 en 3)"),
    ("14:00  ", "Pauze"),
    ("14:15  ", "Trackingsensoren: lijnen zien"),
    ("14:45  ", "Uitdaging: lijn volgen of obstakels ontwijken"),
    ("15:30  ", "Afsluiting en vooruitblik"),
], "De tijden zijn richtlijnen. Botsing vermijden is het belangrijkste onderdeel: daar komt alles samen.")

# ---------------------------------------------------------------- terugblik
s = new(L_TITLE_ONLY, "Opwarmer: wat gebeurt er?",
        "Terugblik op les 4 (±3 min). Eerst voorspellen.\n"
        "Antwoorden: 1) Niets op het scherm: oled.show() ontbreekt.\n"
        "2) De buzzer blijft piepen: duty_u16(0) ontbreekt.\n"
        "3) Er gebeurt niets: de functie wordt gemaakt maar nooit aangeroepen.")
qs = ['oled.text("Hallo", 0, 0)\ntime.sleep(2)',
      "BZ.freq(800)\nBZ.duty_u16(500)\nprint(\"Klaar\")",
      "def piep():\n    BZ.duty_u16(500)\n    time.sleep(0.2)\n    BZ.duty_u16(0)"]
x = 0.8
for k, q in enumerate(qs):
    circle_num(s, x, 1.65, k + 1)
    code(s, x, 2.4, 3.75, q, size=14, h=1.9)
    box(s, x, 4.55, 3.75, 0.9, GREY)
    text(s, x + 0.2, 4.55, 3.35, 0.9, "Wat gebeurt er? …", size=16, color=MUTED, italic=True, anchor=MSO_ANCHOR.MIDDLE)
    x += 4.02
strip_empty(s)

# ---------------------------------------------------------------- wat is een sensor
s = new(L_TITLE_ONLY, "Wat is een sensor?",
        "Kernbegrip (±3 min). Een sensor meet iets uit de omgeving en zet dat om in een getal dat de Pico kan lezen.\n"
        "Drie soorten waarden vandaag: een analoge waarde (0–65535), een afstand in cm en een digitale waarde (0 of 1).\n"
        "Koppeling met les 2: input → if → actie. Nu komt de input niet van het toetsenbord maar van een sensor.")
flow = [("Sensor", "meet iets", "vandaag", RED_T, RED),
        ("Pico", "beslist met if", "les 2", BLUE_T, NAVY),
        ("Actor", "doet iets", "les 4", LILAC_T, NAVY)]
x = 0.8
for k, (h, b, l, f, c) in enumerate(flow):
    box(s, x, 1.75, 3.6, 1.7, f)
    text(s, x + 0.3, 1.85, 3.0, 0.55, h, size=24, bold=True, color=c)
    text(s, x + 0.3, 2.45, 3.0, 0.45, b, size=17)
    text(s, x + 0.3, 2.9, 3.0, 0.45, l, size=15, italic=True, color=MUTED)
    if k < 2:
        text(s, x + 3.62, 2.2, 0.5, 0.8, "→", size=36, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    x += 4.1
sens = [("Lichtsensoren", "0 … 65535", "analoog: veel tussenwaarden"),
        ("Ultrasoon", "bijv. 24 cm", "afstand tot een voorwerp"),
        ("Trackingsensoren", "0 of 1", "digitaal: zwart of wit")]
x = 0.8
for h, v, b in sens:
    box(s, x, 3.8, 3.8, 2.3, GREY)
    text(s, x + 0.25, 3.95, 3.3, 0.45, h, size=18, bold=True, color=NAVY)
    text(s, x + 0.25, 4.5, 3.3, 0.6, v, size=24, bold=True, color=RED, font="Courier New")
    text(s, x + 0.25, 5.25, 3.3, 0.7, b, size=15)
    x += 4.0
strip_empty(s)

# ---------------------------------------------------------------- leerdoelen
s = new(L_TITLE_ONLY, "Leerdoelen van vandaag",
        "Het doel is niet alleen sensoren uitlezen, maar vooral: de robot laten reageren op wat hij meet.")
card(s, 0.8, 1.7, 5.7, 4.4, "Je kunt…", [
    "• uitleggen wat een sensor is", "• lichtsensoren uitlezen (ADC)",
    "• afstand meten met de ultrasone sensor", "• een lijn herkennen met de trackingsensoren",
    "• de robot laten reageren op een sensor"], fill=LILAC_T, size=19)
card(s, 6.9, 1.7, 5.7, 4.4, "Herhaling uit les 2", [
    [("while True:", {"font": "Courier New", "bold": True, "color": RED}), ("  steeds opnieuw meten", {})],
    [("if / else", {"font": "Courier New", "bold": True, "color": RED}), ("  beslissen op basis van de meting", {})],
    [("> <  ==", {"font": "Courier New", "bold": True, "color": RED}), ("  vergelijken met een drempel", {})],
    "", "Meten → beslissen → doen → opnieuw"], fill=BLUE_T, size=19)
strip_empty(s)

website(["Open de website (link hieronder)", "Kies in het menu links Les 5",
         "Per sensor: uitleg, voorbeeldcode, opdracht", "Uitleg van de code via de link onder elk voorbeeld"],
        "Laat de website zien. Wijs op de animaties bij de ultrasone sensor en de trackingsensoren.", IMG_SITE)

# ================================================================ DEEL 1
deel(L_DEEL_A, "Deel 1", "Licht en afstand meten",
     "Start deel 1 (12:45). Robot klaarzetten, Thonny verbonden. Telefoon met zaklamp bij de hand.")

# ---------------------------------------------------------------- lichtsensoren
s = new(L_TITLE_ONLY, "Lichtsensoren: hoe licht is het?",
        "Just-in-time uitleg (±4 min). Een fotoweerstand verandert met de hoeveelheid licht. De ADC (analoog-digitaal-omzetter)\n"
        "maakt daar een getal van tussen 0 en 65535.\n"
        "ADC(27) en ADC(26) zijn de aansluitingen van de twee lichtsensoren.")
pic(s, IMG + "lightsensor1.jpg", 0.8, 1.7, 1.9, 2.1)
pic(s, IMG + "lightsensor2.jpg", 2.9, 1.7, 1.9, 2.1)
# schaal
text(s, 0.8, 4.05, 4.0, 0.4, "Wat geeft de sensor terug?", size=16, bold=True, color=NAVY)
bar = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.55), Inches(4.0), Inches(0.45))
bar.fill.gradient(); bar.fill.gradient_angle = 0
bar.fill.gradient_stops[0].color.rgb = BLACK; bar.fill.gradient_stops[1].color.rgb = RGBColor(0xFF, 0xE8, 0x80)
bar.line.fill.background(); bar.shadow.inherit = False
text(s, 0.8, 5.05, 2.0, 0.4, "0  donker", size=14, bold=True)
text(s, 2.8, 5.05, 2.0, 0.4, "65535  licht", size=14, bold=True, align=PP_ALIGN.RIGHT)
code(s, 5.2, 1.7, 7.4, "from machine import ADC\nimport time\n\nlight1 = ADC(27)     # lichtsensor 1\nlight2 = ADC(26)     # lichtsensor 2\n\nwhile True:\n    l1 = light1.read_u16()\n    l2 = light2.read_u16()\n    print(\"licht1:\", l1, \" licht2:\", l2)\n    time.sleep(0.5)", size=15)
next_step(s, "opdracht lichtsensoren")
strip_empty(s)

doen("Aan de slag: licht meten", [
    ("Opdracht  ", "Lees beide sensoren uit en schijn er met je telefoonlamp op"),
    ("Onderzoek  ", "Wat is de waarde in het donker, in het lokaal en met de lamp?"),
    ("Extra  ", "Print \"links is lichter\" of \"rechts is lichter\" met een if"),
], "Opdracht lichtsensoren (±15 min). Laat ze hun meetwaarden noteren: die hebben ze nodig om een drempel te kiezen.",
    foot="Lesmateriaal: les 5, Lichtsensoren")

# ---------------------------------------------------------------- ultrasoon
s = new(L_TITLE_ONLY, "Ultrasone sensor: afstand meten",
        "Just-in-time uitleg (±4 min). De sensor zendt een onhoorbare geluidspuls uit en meet hoe lang de echo onderweg is.\n"
        "Geluid gaat ongeveer 343 meter per seconde. Afstand = tijd x snelheid / 2 (heen en terug).\n"
        "De animatie speelt alleen in de diavoorstelling.")
pic(s, IMG + "ultrasoonsensor.jpg", 0.8, 1.7, 5.6, 2.1)
pic(s, IMG + "ultrasonic-sensor-working2.gif", 0.8, 3.95, 2.9, 2.3)
card(s, 3.9, 3.95, 2.5, 2.3, "Echo", ["zender → voorwerp", "→ ontvanger", "tijd → afstand"], fill=BLUE_T, size=14, head_size=17)
code(s, 6.8, 1.7, 5.8, "from pico_car import ultrasonic\nimport time\n\nsonar = ultrasonic()\n\nwhile True:\n    afstand = sonar.Distance_accurate()\n    print(\"afstand:\", afstand, \"cm\")\n    time.sleep(1)", size=15)
box(s, 6.8, 4.9, 5.8, 1.2, GREY)
text(s, 7.0, 4.9, 5.4, 1.2, [[("Distance_accurate()", {"font": "Courier New", "bold": True, "color": RED}),
                              (" geeft de afstand in centimeters.", {})]], size=16, anchor=MSO_ANCHOR.MIDDLE)
next_step(s, "opdracht 1: afstand meten")
strip_empty(s)

doen("Aan de slag: opdracht 1", [
    ("Opdracht  ", "Meet de afstand tot je hand op verschillende afstanden"),
    ("Onderzoek  ", "Wat is de kleinste en de grootste afstand die klopt?"),
    ("Onderzoek  ", "Werkt het ook met een zachte trui of een schuin boek?"),
], "Opdracht 1 (±10 min). Zachte en schuine oppervlakken kaatsen het geluid slecht terug: goede discussie over meetfouten.",
    foot="Lesmateriaal: les 5, Ultrasone sensor")

# ---------------------------------------------------------------- botsing vermijden
s = new(L_TITLE_ONLY, "Meten, beslissen, doen",
        "Just-in-time uitleg (±5 min). Hier komt alles samen: de while-loop meet steeds opnieuw, de if beslist, de motor doet.\n"
        "In het basisbestand van de handleiding staat onder if en else nog pass: dat vervangen ze door hun eigen code.\n"
        "Bespreek de drempel van 20 cm en de sleep(1): te lang wachten = te laat remmen. Probeer 0.1.")
code(s, 0.8, 1.7, 6.8, "while True:\n    afstand = sonar.Distance_accurate()\n\n    if afstand > 20:\n        Motor.Car_Run(150, 150)   # rijden\n    else:\n        Motor.Car_Stop()          # stop\n\n    time.sleep(0.1)", size=16)
steps3 = [("Meten", "sonar.Distance_accurate()", LILAC_T), ("Beslissen", "if afstand > 20:", BLUE_T),
          ("Doen", "Car_Run() of Car_Stop()", RED_T)]
y = 1.7
for k, (h, c_, f) in enumerate(steps3):
    box(s, 8.0, y, 4.6, 1.15, f)
    circle_num(s, 8.2, y + 0.3, k + 1, fill=NAVY, d=0.55, size=17)
    text(s, 8.95, y + 0.12, 3.5, 0.45, h, size=19, bold=True, color=NAVY)
    text(s, 8.95, y + 0.58, 3.5, 0.45, c_, size=12, font="Courier New", bold=True)
    y += 1.3
text(s, 8.0, y + 0.05, 4.6, 0.6, "↻  en weer opnieuw, 10 keer per seconde", size=15, italic=True, color=MUTED)
next_step(s, "opdracht 2 en 3")
strip_empty(s)

doen("Aan de slag: opdracht 2 en 3", [
    ("2  ", "Rij vooruit en stop als er iets dichter dan 20 cm is"),
    ("3  ", "Next level: stop, draai een stukje en rij weer verder"),
    ("Extra  ", "Laat de LED of buzzer waarschuwen als het dichtbij komt"),
], "Opdracht 2 en 3 (tot de pauze). Veiligheid: test op de grond, met een boek of tas als obstakel.\n"
   "Opdracht 3 combineert Car_Stop, Car_Left/Right en sleep in de else.",
    foot="Lesmateriaal: les 5, Ultrasone sensor")

pauze("Pauze\n14:15 verder met deel 2",
      "Pauze (14:00–14:15). Robot uit (schakelaar OFF). Zet in de pauze een stuk zwarte tape op een witte ondergrond klaar.")

# ================================================================ DEEL 2
deel(L_DEEL_B, "Deel 2", "Lijnen zien met de trackingsensoren",
     "Start deel 2 (14:15). Zorg voor witte vellen of een witte vloer met zwarte tape.")

# ---------------------------------------------------------------- trackingsensoren
s = new(L_TITLE_ONLY, "Trackingsensoren: zwart of wit?",
        "Just-in-time uitleg (±5 min). Elke sensor zendt infrarood licht uit en meet hoeveel er terugkaatst.\n"
        "Wit kaatst veel terug (1), zwart weinig (0). Infrarood is onzichtbaar, maar een telefooncamera ziet het als paars licht.\n"
        "Laat iemand het met de telefoon proberen. De ledjes boven op de robot gaan uit boven zwart.")
pic(s, IMG + "trackingsensors.jpg", 0.8, 1.7, 6.0, 2.4)
pic(s, IMG + "infraroodsensor.gif", 0.8, 4.3, 1.6, 2.0)
card(s, 2.6, 4.3, 4.2, 2.0, "Probeer het zelf", ["Kijk met je telefooncamera", "naar de sensoren: je ziet", "zwak paars licht."],
     fill=BLUE_T, size=14, head_size=16)
vals = [("wit", "1", WHITE, NAVY), ("zwart", "0", BLACK, WHITE)]
y = 1.7
for naam, v, f, c in vals:
    b = box(s, 7.2, y, 2.4, 1.4, f)
    b.line.color.rgb = RGBColor(0x99, 0x99, 0x99); b.line.width = Pt(1)
    text(s, 7.2, y + 0.1, 2.4, 0.5, naam, size=18, bold=True, color=c, align=PP_ALIGN.CENTER)
    text(s, 7.2, y + 0.55, 2.4, 0.8, v, size=36, bold=True, color=c, align=PP_ALIGN.CENTER, font="Courier New")
    y += 1.6
card(s, 9.9, 1.7, 2.7, 3.0, "4 sensoren", ["T1 T2 T3 T4", "van links", "naar rechts"], fill=LILAC_T, size=15)
text(s, 7.2, 5.0, 5.4, 1.2, ["Werkt alleen op korte afstand", "boven de grond (een paar mm)."], size=15, italic=True, color=MUTED)
strip_empty(s)

# ---------------------------------------------------------------- tracking code + patronen
s = new(L_TITLE_ONLY, "Van sensorwaarden naar sturen",
        "Uitleg (±5 min). De code leest de vier sensoren uit. Bespreek daarna samen de tabel: welke kant moet de robot op?\n"
        "Dit is de denkstap voor de uitdaging lijn volgen. Laat studenten de tabel zelf aanvullen voordat je de antwoorden noemt.\n"
        "Een uitgewerkt voorbeeld staat in VisualCode_RaspberryPico/3.Robotics course/4.Car tracking.py.")
code(s, 0.8, 1.7, 6.0, "from machine import Pin\nimport time\n\nT1 = Pin(2, Pin.IN)   # links\nT2 = Pin(3, Pin.IN)\nT3 = Pin(4, Pin.IN)\nT4 = Pin(5, Pin.IN)   # rechts\n\nwhile True:\n    print(T1.value(), T2.value(),\n          T3.value(), T4.value())\n    time.sleep(0.1)", size=15)
text(s, 7.2, 1.7, 5.4, 0.45, "Wat moet de robot doen?", size=19, bold=True, color=NAVY)
rows = [("1 0 0 1", "lijn in het midden", "rechtdoor"), ("0 0 1 1", "lijn links", "bocht links"),
        ("1 1 0 0", "lijn rechts", "bocht rechts"), ("1 1 1 1", "geen lijn", "?")]
y = 2.25
for v, b, a in rows:
    box(s, 7.2, y, 5.4, 0.78, GREY)
    text(s, 7.35, y, 1.6, 0.78, v, size=16, bold=True, font="Courier New", color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 8.95, y, 2.0, 0.78, b, size=14, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 10.95, y, 1.6, 0.78, a, size=15, bold=True, color=RED, anchor=MSO_ANCHOR.MIDDLE)
    y += 0.88
text(s, 7.2, y + 0.05, 5.4, 0.5, "0 = zwart (lijn)   1 = wit", size=14, italic=True, color=MUTED)
next_step(s, "opdracht trackingsensoren")
strip_empty(s)

doen("Aan de slag: lijnen zien", [
    ("Opdracht  ", "Lees de vier sensoren uit en beweeg de robot met de hand over de lijn"),
    ("Kijk ook  ", "naar de ledjes boven op de robot"),
    ("Uitdaging  ", "laat de robot zelf de lijn volgen (gebruik de tabel)"),
    ("Of  ", "maak opdracht 3 af: obstakels ontwijken"),
], "Opdracht tracking (±15 min) en daarna de uitdaging (tot ±15:30). Lijn volgen: begin langzaam (snelheid 80–120).\n"
   "Studenten kiezen zelf: lijn volgen of obstakels ontwijken.",
    foot="Lesmateriaal: les 5, Trackingsensoren")

# ---------------------------------------------------------------- hulpkaart
s = new(L_TITLE_ONLY, "Hulpkaart: de sensor doet raar",
        "Kan blijven staan tijdens het werken.")
kaartgrid(s, [
    ("Waarde verandert niet", ["Juiste pin? ADC(27), ADC(26)", "Schijn recht op de sensor"]),
    ("IndentationError", ["Lege if of else?", "Zet er tijdelijk pass neer"]),
    ("Robot remt te laat", ["sleep(1) is te lang", "Probeer time.sleep(0.1)"]),
    ("Afstand klopt niet", ["Zachte of schuine dingen", "kaatsen slecht terug"]),
    ("Tracking altijd 1", ["Robot te hoog of op glans?", "Batterijen bijna leeg?"]),
    ("Lijn kwijt", ["Rij langzamer", "Bocht scherper maken"]),
])
strip_empty(s)

# ---------------------------------------------------------------- afsluiting
s = new(L_TITLE_ONLY, "Afsluiting: wat kun je nu?",
        "Afsluiting (15:30, ±10 min). Laat een robot zien die obstakels ontwijkt en een die een lijn volgt.\n"
        "Vooruitblik: in les 6 maak je je eigen robot-werktuig. Schakelaar op OFF.")
checklist(s, 0.8, 1.75, ["Uitleggen wat een sensor is", "Licht meten met de ADC", "Afstand meten met ultrasoon",
                         "Zwart en wit zien met tracking", "Meten → beslissen → doen", "Een robot die zelf reageert"])
box(s, 6.9, 1.7, 5.7, 4.5, BLUE_T)
text(s, 7.15, 1.85, 5.2, 0.5, "Volgende week: les 6", size=20, bold=True, color=NAVY)
text(s, 7.15, 2.5, 5.2, 1.0, "Maak je eigen robot-werktuig", size=24, bold=True, color=RED)
text(s, 7.15, 3.6, 5.2, 2.0, ["Je combineert alles wat je hebt geleerd:", "motoren, actoren en sensoren,",
                              "in een eigen ontwerp."], size=17)
strip_empty(s)

afronden(OUT, "Vragen? Schakelaar op OFF en de robot veilig opbergen.")
