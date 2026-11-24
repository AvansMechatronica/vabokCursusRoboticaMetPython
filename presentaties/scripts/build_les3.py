"""Bouwt presentaties/les3.pptx: Bouw en programmeer je eerste robot.
Gebruik: python build_les3.py <repo-root> <uitvoer.pptx> <screenshot-website.png>"""
import os, sys
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "helpers.py"), encoding="utf-8").read())
from PIL import Image

IMG = ROOT + "/documentation/images/"
MNT = IMG + "mounting/"
URL = "https://avansmechatronica.github.io/vabokCursusRoboticaMetPython/"
IMG_SITE = sys.argv[3]


def pic(slide, path, x, y, w, h, border=False, align="center"):
    """Plaats afbeelding passend binnen kader (x, y, w, h), beeldverhouding behouden."""
    iw, ih = Image.open(path).size
    scale = min(w / iw, h / ih)
    pw, phh = iw * scale, ih * scale
    px = x + (w - pw) / 2 if align == "center" else x
    py = y + (h - phh) / 2
    p = slide.shapes.add_picture(path, Inches(px), Inches(py), Inches(pw), Inches(phh))
    if border:
        p.line.color.rgb = RGBColor(0xBB, 0xBB, 0xBB); p.line.width = Pt(0.75)
    return p


# ---------------------------------------------------------------- 1 titel
title_slide = prs.slides[0]
for p in title_slide.placeholders:
    if p.placeholder_format.idx == 21:
        runs = p.text_frame.paragraphs[0].runs
        runs[0].text = "Les "
        runs[1].text = "3: Bouw en programmeer je eerste robot"
title_slide.notes_slide.notes_text_frame.text = (
    "Welkom. Vandaag bouw je je eigen Pico-robot en laat je hem voor het eerst rijden.\n"
    "Belangrijk: eerst bouwen, dan laten controleren door de docent, dan pas krijg je de geprogrammeerde Raspberry Pi Pico.")

# ---------------------------------------------------------------- 2 planning
s = new(L_AGENDA, "Vandaag",
        "De tijden zijn richtlijnen. Bouwen gaat niet bij iedereen even snel: wie klaar is, laat de robot controleren en gaat door met programmeren.")
set_lines(ph(s, 21).text_frame, [
    ("12:30  ", "Introductie, werkwijze en veiligheid"),
    ("12:45  ", "Uitleenovereenkomst tekenen, deel 1 – bouwen"),
    ("", "Klaar? Controle door de docent + Pico ophalen"),
    ("14:00  ", "Pauze"),
    ("14:15  ", "Deel 2 – Thonny en je eerste robotprogramma"),
    ("14:45  ", "Opdrachten 1–4: bewegingen en patronen"),
    ("15:30  ", "Afsluiting en vooruitblik"),
], size=19, space_after=12)
strip_empty(s)

# ---------------------------------------------------------------- 3 van python naar robot
s = new(L_TITLE_ONLY, "Van Python naar robot",
        "Terugblik op les 2 (±3 min). Vorige week schreef je Python op de computer; vandaag stuur je met dezelfde taal echte motoren aan.\n"
        "Checkvraag: 'Wat doet time.sleep(5) volgens jou?' Laat ze voorspellen voordat je het uitlegt.")
text(s, 0.8, 1.7, 5.6, 0.5, "Les 2: op de computer", size=20, bold=True, color=NAVY)
code(s, 0.8, 2.3, 5.6, 'naam = "Robbie"\nprint("Hallo " + naam)', size=18, h=1.5)
text(s, 0.8, 4.0, 5.6, 1.5, ["Python zet tekst op het scherm."], size=17)
text(s, 6.45, 2.6, 0.5, 0.8, "→", size=40, bold=True, color=RED, align=PP_ALIGN.CENTER)
text(s, 7.0, 1.7, 5.6, 0.5, "Les 3: op de robot", size=20, bold=True, color=RED)
code(s, 7.0, 2.3, 5.6, 'Motor.Car_Run(255, 255)\ntime.sleep(5)\nMotor.Car_Stop()', size=18, h=1.5)
text(s, 7.0, 4.0, 5.6, 1.5, ["Python laat de motoren 5 seconden draaien."], size=17)
box(s, 0.8, 5.1, 11.8, 1.0, GREY)
text(s, 1.05, 5.1, 11.3, 1.0, [[("Zelfde taal, nieuw doel: ", {"bold": True, "color": NAVY}),
                                ("variabelen, loops en if-statements gebruik je straks ook op de robot.", {})]],
     size=18, anchor=MSO_ANCHOR.MIDDLE)
strip_empty(s)

# ---------------------------------------------------------------- 4 leerdoelen
s = new(L_TITLE_ONLY, "Leerdoelen van vandaag",
        "Noem de twee delen: bouwen en programmeren. De Pico wordt door de docent geprogrammeerd, dus firmware en bibliotheek installeren hoeft niet.")
card(s, 0.8, 1.7, 5.7, 3.9, "Deel 1 – Bouwen",
     ["• De Pico-robot correct in elkaar zetten", "• De onderdelen herkennen en benoemen",
      "• Kabels aansluiten volgens het aansluitdiagram"], fill=LILAC_T, size=20)
card(s, 6.9, 1.7, 5.7, 3.9, "Deel 2 – Programmeren",
     ["• Thonny gebruiken en verbinden met de Pico", "• Een programma schrijven dat de robot laat rijden",
      "• Code opslaan en uitvoeren op de Pico", "• De robot veilig testen en problemen oplossen"],
     fill=BLUE_T, size=20)
strip_empty(s)

# ---------------------------------------------------------------- 5 werkwijze: 4 stappen
s = new(L_TITLE_ONLY, "Zo werken we vandaag",
        "Belangrijkste dia van de introductie. Leg de volgorde nadrukkelijk uit:\n"
        "1) uitleenovereenkomst tekenen en bouwpakket ophalen, 2) bouwen met de handleiding, 3) controle door de docent,\n"
        "4) je krijgt de geprogrammeerde Pico, 5) pas dan programmeren.\n"
        "Zonder getekende uitleenovereenkomst (support/uitleenovereenkomst.docx) geen bouwpakket.\n"
        "Reden voor de controle: een verkeerd aangesloten kabel of omgekeerde batterij kan de Pico beschadigen. En: de robot wordt maar één keer verstrekt.")
steps = [("Ophalen", "Teken de uitleenovereenkomst en haal je bouwpakket op.", GREY, NAVY),
         ("Bouwen", "Zet de robot in elkaar met de online bouwstappen.", LILAC_T, NAVY),
         ("Controle", "Steek je hand op: de docent controleert je robot.", RED_T, RED),
         ("Pico ophalen", "Na goedkeuring krijg je de geprogrammeerde Pico.", BLUE_T, NAVY),
         ("Programmeren", "Pas nu ga je de robot programmeren en testen.", GREEN_T, GREEN)]
x = 0.8
for k, (h, b, f, c) in enumerate(steps):
    box(s, x, 1.8, 2.12, 3.2, f)
    circle_num(s, x + 0.2, 2.0, k + 1, fill=c)
    text(s, x + 0.2, 2.75, 1.8, 0.5, h, size=17, bold=True, color=c)
    text(s, x + 0.2, 3.3, 1.8, 1.6, b, size=14)
    if k < 4:
        text(s, x + 2.1, 2.95, 0.32, 0.8, "→", size=24, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    x += 2.42
box(s, 0.8, 5.3, 11.8, 0.85, RED_T)
text(s, 1.05, 5.3, 11.3, 0.85, [[("Let op: ", {"bold": True, "color": RED}),
                                 ("je krijgt de robot maar één keer. Is hij kapot, dan deel je er een met een andere student.", {})]],
     size=17, anchor=MSO_ANCHOR.MIDDLE)
strip_empty(s)

# ---------------------------------------------------------------- 6 lesmateriaal online
s = new(L_TITLE_ONLY, "Het lesmateriaal: alle stappen online",
        "Laat de website live zien. Les 3 staat in het menu links; de bouwstappen zijn een aparte pagina via de link 'Bekijk de bouwstappen hier'.\n"
        "URL: " + URL)
stappen = ["Open de website (link hieronder)", "Kies in het menu links Les 3",
           "Klik op 'Bekijk de bouwstappen hier'", "Volg de stappen op volgorde"]
y = 1.8
for k, st in enumerate(stappen):
    circle_num(s, 0.8, y, k + 1, d=0.5, size=17)
    text(s, 1.5, y, 4.7, 0.5, st, size=18, anchor=MSO_ANCHOR.MIDDLE)
    y += 0.85
p_ = pic(s, IMG_SITE, 6.6, 1.6, 6.0, 4.1, border=True)
p_.click_action.hyperlink.address = URL
ub = box(s, 0.8, 5.9, 11.8, 0.65, LILAC_T, radius=0.3)
tf = ub.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = URL.replace("https://", "").rstrip("/")
r.font.size = Pt(22); r.font.bold = True; r.font.color.rgb = NAVY
r.hyperlink.address = URL
strip_empty(s)

# ================================================================ DEEL 1
s = new(L_DEEL_A, "Deel 1",
        "Start deel 1 (12:45). Laat iedereen eerst de uitleenovereenkomst tekenen (support/uitleenovereenkomst.docx); pas daarna het bouwpakket uitreiken.\n"
        "De Raspberry Pi Pico krijgen ze nog NIET.")
set_lines(ph(s, 21).text_frame, ["De robot bouwen"], size=22)
strip_empty(s)

# ---------------------------------------------------------------- wat is de pico-robot
s = new(L_TITLE_ONLY, "Wat is de Pico-robot?",
        "Kort (±3 min). De Raspberry Pi Pico is een microcontroller: een klein computertje dat apparaten aanstuurt.\n"
        "Sensoren (waarnemen) en actoren (iets doen) komen in les 4 en 5 uitgebreid terug.")
pic(s, IMG + "pico-robot.png", 0.8, 1.7, 4.6, 4.4)
parts = [("Raspberry Pi Pico", "het brein: voert jouw Python-code uit"),
         ("Motoren en wielen", "om te rijden en te draaien"),
         ("Sensoren", "ultrasoon (afstand) en lijnvolgsensoren"),
         ("LEDs, buzzer, OLED-scherm", "licht, geluid en tekst"),
         ("Batterijen", "stroom als de USB-kabel los is")]
y = 1.75
for k, (h, b) in enumerate(parts):
    circle_num(s, 5.9, y + 0.05, k + 1, fill=RED if k == 0 else NAVY, d=0.5, size=16)
    text(s, 6.6, y, 6.0, 0.45, h, size=19, bold=True, color=NAVY)
    text(s, 6.6, y + 0.42, 6.0, 0.4, b, size=16)
    y += 0.9
strip_empty(s)

# ---------------------------------------------------------------- inhoud doos
s = new(L_TITLE_ONLY, "Eerst: is alles compleet?",
        "Laat studenten de inhoud van de doos naast deze afbeeldingen leggen voordat ze beginnen. Ontbreekt er iets? Meteen melden.\n"
        "Kleine schroefjes en afstandsbusjes in een bakje of dekseltje bewaren.")
inh = ["Inhoud-1.png", "Inhoud-2.png", "Inhoud-3.png", "Inhoud-4.png"]
for k, f in enumerate(inh):
    cx = 0.8 + (k % 2) * 6.0
    cy = 1.65 + (k // 2) * 2.05
    box(s, cx, cy, 5.8, 1.9, GREY)
    pic(s, MNT + f, cx + 0.15, cy + 0.1, 5.5, 1.7)
pill(s, 0.8, 6.0, 7.2, "Tip: bewaar kleine schroefjes in een bakje", fill=NAVY)
strip_empty(s)

# ---------------------------------------------------------------- bouwstappen overzicht
s = new(L_TITLE_ONLY, "De bouwstappen in vogelvlucht",
        "Overzicht (±2 min). Alle details en grotere afbeeldingen staan in de online handleiding.\n"
        "Stap 5: de Raspberry Pi Pico krijg je pas na de controle. Bouw de rest al wel af en laat de plek voor de Pico vrij.")
stp = [("Montage-1.png", "1  Motoren"), ("Montage-2.png", "2  Stuurwiel"), ("Montage-3.png", "3  Zijwielen"),
       ("Montage-4.png", "4  OLED + Bluetooth"), ("Montage-5.png", "5  Raspberry Pi Pico"), ("Montage-6.png", "6  Batterij")]
for k, (f, lbl) in enumerate(stp):
    cx = 0.8 + (k % 3) * 4.0
    cy = 1.6 + (k // 3) * 2.45
    box(s, cx, cy, 3.8, 2.3, GREY)
    pic(s, MNT + f, cx + 0.15, cy + 0.1, 3.5, 1.65)
    text(s, cx + 0.2, cy + 1.8, 3.4, 0.45, lbl, size=16, bold=True, color=RED if k == 4 else NAVY)
text(s, 0.8, 6.5, 11.8, 0.4, "Stap 5: de Pico krijg je van de docent na de controle  ·  Stap 7: aansluitdiagram", size=14,
     italic=True, color=MUTED)
strip_empty(s)

# ---------------------------------------------------------------- stap 1 let op
s = new(L_TITLE_ONLY, "Let op bij stap 1: de motoren",
        "Just-in-time tip: dit is de meest gemaakte fout bij het bouwen. Een verkeerd gemonteerde motor betekent later alles weer uit elkaar halen.\n"
        "Laat de afbeelding rechts zien en wijs de smalle sleuf en de tinnen strip aan.")
pic(s, MNT + "Montage-1.png", 0.8, 1.7, 6.2, 4.4)
pic(s, MNT + "Montage-1a.png", 7.2, 1.7, 2.6, 4.4)
card(s, 10.0, 1.7, 2.6, 4.4, "Check",
     ["De kant zonder tandwiel met de smalle sleuf…", "…komt bij de tinnen strip op de bodemplaat."],
     fill=RED_T, head_color=RED, size=15)
strip_empty(s)

# ---------------------------------------------------------------- aansluitdiagram
s = new(L_TITLE_ONLY, "Stap 7: aansluiten volgens het diagram",
        "Laat de twee aansluitafbeeldingen zien. Kabels kunnen maar op één manier goed: controleer de kleuren en de richting van de stekker.\n"
        "Dit is precies wat de docent bij de controle bekijkt.")
for k, f in enumerate(("Aansluiten-1.png", "Aansluiten-2.png")):
    cx = 0.8 + k * 6.0
    box(s, cx, 1.6, 5.8, 4.6, GREY)
    pic(s, MNT + f, cx + 0.15, 1.7, 5.5, 4.4)
next_step(s, "bouwen met de online handleiding")
strip_empty(s)

doen("Aan de slag: bouw je robot", [
    ("0  ", "Uitleenovereenkomst getekend en bouwpakket opgehaald?"),
    ("1  ", "Bouw de robot met de online bouwstappen"),
    ("2  ", "Beantwoord: waar zitten de motoren, welke sensor zit voorop, waar komt de Pico, hoeveel wielen, waar gaan de batterijen?"),
    ("3  ", "Klaar? Schakelaar op OFF en steek je hand op voor de controle"),
], "Bouwen (tot ±14:00). Loop rond, let vooral op de motoren (stap 1) en de kabels (stap 7).\n"
   "Wie klaar is: controle afnemen (volgende dia) en Pico uitgeven.",
    foot="Lesmateriaal: les 3, stap 1 en de bouwstappen")

# ---------------------------------------------------------------- controle
s = new(L_TITLE_ONLY, "Stop! Eerst laten controleren",
        "Controlemoment per student/groep. Loop de checklist langs; pas als alles klopt, geef je de geprogrammeerde Raspberry Pi Pico uit.\n"
        "Noteer eventueel wie een Pico heeft gekregen.")
checks = ["Motoren goed gemonteerd (sleuf bij tinnen strip)", "Wielen draaien vrij en zitten vast",
          "Alle kabels volgens het aansluitdiagram", "Batterijhouder goed aangesloten", "Schakelaar staat op OFF",
          "Geen losse schroefjes of onderdelen"]
text(s, 0.8, 1.65, 6.4, 0.5, "De docent controleert:", size=20, bold=True, color=NAVY)
y = 2.25
for c in checks:
    circle_num(s, 0.8, y + 0.02, "✓", fill=GREEN, d=0.42, size=14)
    text(s, 1.4, y, 5.8, 0.5, c, size=17, anchor=MSO_ANCHOR.MIDDLE)
    y += 0.65
box(s, 7.6, 1.7, 5.0, 4.4, NAVY)
text(s, 7.9, 1.95, 4.4, 0.6, "Goedgekeurd?", size=24, bold=True, color=WHITE)
text(s, 7.9, 2.7, 4.4, 2.0, ["Je krijgt de Raspberry Pi Pico met de software er al op.",
                             "Monteer hem (stap 5) en ga door naar deel 2."], size=18, color=WHITE)
pill(s, 7.9, 5.25, 4.4, "Pas daarna: programmeren", fill=RED)
strip_empty(s)

# ---------------------------------------------------------------- pauze
s = new(L_PAUZE, "Pauze\n14:15 verder met deel 2",
        "Pauze (14:00–14:15). Wie nog bouwt, kan na de pauze afronden en laten controleren; de anderen starten met Thonny.")
strip_empty(s)

# ================================================================ DEEL 2
s = new(L_DEEL_B, "Deel 2",
        "Start deel 2 (14:15). Alleen studenten met een gecontroleerde robot en een Pico gaan programmeren. Anderen kunnen Thonny alvast installeren.")
set_lines(ph(s, 21).text_frame, ["Thonny en je eerste robotprogramma"], size=22)
strip_empty(s)

# ---------------------------------------------------------------- thonny
s = new(L_TITLE_ONLY, "Thonny: verbinden met de Pico",
        "Just-in-time uitleg (±5 min), live voordoen. Thonny is een Python-programma speciaal voor beginners.\n"
        "Valkuil: rechtsonder staat de interpreter nog op de lokale Python; kies MicroPython (Raspberry Pi Pico).\n"
        "Werkt de verbinding niet? Andere USB-kabel proberen (sommige kabels laden alleen op).")
stp = ["Installeer Thonny via thonny.org (als dat nog niet is gedaan)",
       "Sluit de Pico aan met de USB-kabel",
       "Kies rechtsonder: MicroPython (Raspberry Pi Pico)",
       "Zie je >>> in de Shell? Dan werkt de verbinding"]
y = 1.75
for k, st in enumerate(stp):
    circle_num(s, 0.8, y, k + 1, d=0.5, size=17)
    text(s, 1.5, y - 0.05, 4.9, 0.7, st, size=17, anchor=MSO_ANCHOR.MIDDLE)
    y += 0.85
code(s, 0.8, 5.25, 5.6, '>>> print("Hello, Robot!")\nHello, Robot!', size=16)
pic(s, IMG + "thony_hello_world.png", 6.8, 1.6, 5.8, 4.7, border=True)
strip_empty(s)

# ---------------------------------------------------------------- veiligheid
s = new(L_TITLE_ONLY, "Veilig testen",
        "Lees deze regels samen voordat iemand op Run drukt. Het belangrijkste: test op de grond, nooit op een tafel zonder rand.\n"
        "Begin met een lage snelheid en een korte tijd.")
veilig = [("Op de grond", "Test op de vloer of een grote, lege tafel, ver van randen en trappen."),
          ("Handen weg", "Vingers, haren en losse kleding uit de buurt van de wielen."),
          ("Vrije baan", "Geen kabels, tassen of mensen op de rijroute."),
          ("Rustig beginnen", "Eerst lage snelheid en korte tijd. Onverwacht gedrag? Schakelaar op OFF."),
          ("USB-verlengkabel", "Zo kan de robot een stukje rijden terwijl hij verbonden is."),
          ("Zuinig zijn", "Je krijgt de robot maar één keer.")]
for k, (h, b) in enumerate(veilig):
    cx = 0.8 + (k % 3) * 4.0
    cy = 1.65 + (k // 3) * 2.3
    card(s, cx, cy, 3.8, 2.1, h, [b], fill=RED_T if k < 3 else GREY, head_color=RED if k < 3 else NAVY, size=15)
strip_empty(s)

# ---------------------------------------------------------------- eerste programma
s = new(L_TITLE_ONLY, "Je eerste robotprogramma",
        "Just-in-time uitleg (±5 min). Loop de code regel voor regel door.\n"
        "Let op de schrijfwijze: from pico_car import pico_car (kleine letters), net als in de voorbeeldcode op de Pico.\n"
        "Checkvraag: 'Wat verander je om de robot 2 seconden te laten rijden?'")
code(s, 0.8, 1.65, 6.6, "from pico_car import pico_car\nimport time\n\nMotor = pico_car()\n\nprint(\"Robot start!\")\nMotor.Car_Run(255, 255)  # links, rechts\ntime.sleep(5)            # 5 seconden\nMotor.Car_Stop()\nprint(\"Robot gestopt!\")",
     size=16)
uitleg = [("import", "haal de robotbibliotheek en de timer op"),
          ("Motor = pico_car()", "maak de motorbesturing klaar"),
          ("Car_Run(255, 255)", "rij vooruit; snelheid 0–255 per motor"),
          ("time.sleep(5)", "wacht 5 seconden, de robot rijdt door"),
          ("Car_Stop()", "stop de motoren, vergeet hem nooit!")]
y = 1.65
for h, b in uitleg:
    box(s, 7.7, y, 4.9, 0.82, GREY)
    text(s, 7.9, y + 0.05, 4.5, 0.4, h, size=15, bold=True, color=RED, font="Courier New")
    text(s, 7.9, y + 0.42, 4.5, 0.4, b, size=14)
    y += 0.92
next_step(s, "programma overtypen en opslaan")
strip_empty(s)

# ---------------------------------------------------------------- opslaan en uitvoeren
s = new(L_TITLE_ONLY, "Opslaan en uitvoeren",
        "Leg het verschil uit: met Run (F5) start je het programma vanuit Thonny, de USB-kabel moet dan aangesloten zijn.\n"
        "Wil je dat de robot zonder computer start? Sla op als main.py. Er kan maar één main.py zijn.\n"
        "Waarschuw: pico_car.py nooit verwijderen of overschrijven.")
card(s, 0.8, 1.7, 5.7, 3.6, "A  Direct uitvoeren (testen)",
     ["• File → Save as… → Raspberry Pi Pico", "• Naam: test_vooruit.py", "• Batterijen erin, schakelaar ON",
      "• Klik op de groene Run-knop of druk F5"], fill=BLUE_T, size=17)
card(s, 6.9, 1.7, 5.7, 3.6, "B  Automatisch starten",
     ["• Sla op als main.py op de Pico", "• Start bij aanzetten, ook zonder USB", "• Er kan maar één main.py zijn",
      "• Verwijderen: View → Files, rechtsklik"], fill=LILAC_T, size=17)
box(s, 0.8, 5.5, 11.8, 0.75, RED_T)
text(s, 1.05, 5.5, 11.3, 0.75, [[("Nooit verwijderen: ", {"bold": True, "color": RED}),
                                 ("pico_car.py", {"font": "Courier New", "bold": True}),
                                 (" – daarin staan alle functies om de robot aan te sturen.", {})]],
     size=17, anchor=MSO_ANCHOR.MIDDLE)
strip_empty(s)

doen("Aan de slag: eerste test", [
    ("Test 1  ", "Laat de robot 5 seconden vooruit rijden. Klopt de tijd?"),
    ("Test 2  ", "Rij langzamer: Car_Run(100, 100)"),
    ("Test 3  ", "Links sneller dan rechts: Car_Run(200, 100). Wat gebeurt er?"),
], "Eerste test (±15 min). Rijdt de robot achteruit? Dan zijn de motordraadjes omgedraaid. Rijdt hij scheef? Dat is normaal, corrigeren in de code.",
    foot="Lesmateriaal: les 3, stap 4 t/m 6")

# ---------------------------------------------------------------- functies
s = new(L_TITLE_ONLY, "Bewegen met pico_car",
        "Just-in-time uitleg (±4 min) voor de opdrachten. Draaien kan op twee manieren: met Car_Left/Car_Right (draaien op de plek)\n"
        "of met Car_Run en verschillende snelheden (een bocht).\n"
        "De tijd voor een draai van 90 graden moet je zelf uitproberen: dat hangt af van de batterijen en de ondergrond.")
fn = [("Car_Run(l, r)", "vooruit"), ("Car_Back(l, r)", "achteruit"), ("Car_Left(l, r)", "draai links"),
      ("Car_Right(l, r)", "draai rechts"), ("Car_Stop()", "stop")]
y = 1.7
for f, b in fn:
    box(s, 0.8, y, 6.0, 0.72, GREY)
    text(s, 1.0, y, 3.4, 0.72, "Motor." + f, size=16, bold=True, color=NAVY, font="Courier New", anchor=MSO_ANCHOR.MIDDLE)
    text(s, 4.6, y, 2.1, 0.72, b, size=16, anchor=MSO_ANCHOR.MIDDLE)
    y += 0.86
card(s, 7.2, 1.7, 5.4, 1.95, "Snelheid: 0 – 255", ["l = linkermotor, r = rechtermotor",
                                                  "Te laag? Dan blijft de robot staan."], fill=BLUE_T, size=16)
card(s, 7.2, 3.85, 5.4, 2.45, "Bocht maken", [[("Car_Run(255, 128)", {"font": "Courier New", "bold": True}), ("  → naar rechts", {})],
                                             [("Car_Run(128, 255)", {"font": "Courier New", "bold": True}), ("  → naar links", {})],
                                             "De snelste kant gaat de bocht om."], fill=LILAC_T, size=15)
next_step(s, "opdrachten 1–4")
strip_empty(s)

doen("Aan de slag: opdracht 1 t/m 4", [
    ("1  Bewegingen  ", "vooruit/achteruit, bocht, zigzag"),
    ("2  Snelheid  ", "drie snelheden, cirkel, minimale snelheid"),
    ("3  Patronen  ", "vierkant, driehoek, achtje"),
    ("4  Uitdaging  ", "vooruit, 360° draaien en terug naar het begin"),
    ("Tip: ", "gebruik een for-loop uit les 2 voor herhalingen"),
], "Opdrachten (tot ±15:30). Moedig aan om een logboek bij te houden: welke snelheid en tijd geeft een draai van 90 graden?\n"
   "Snelle studenten: extra uitdagingen A–D in de handleiding.",
    foot="Lesmateriaal: les 3, opdrachten 1–4")

# ---------------------------------------------------------------- troubleshooting
s = new(L_TITLE_ONLY, "Hulpkaart: de robot doet het niet",
        "Kan blijven staan tijdens de opdrachten. Verwijs ernaar voordat je zelf komt helpen.")
probl = [("Beweegt niet", ["Batterijen erin, schakelaar ON?", "Motorkabels goed vast?"]),
         ("Rijdt achteruit", ["Motordraadjes omgedraaid", "Vraag de docent om hulp"]),
         ("Rijdt niet recht", ["Normaal! Corrigeer in de code:", "Car_Run(220, 255)"]),
         ("ImportError", ["Schrijf pico_car met kleine letters", "pico_car.py nog op de Pico?"]),
         ("Stopt niet", ["Car_Stop() vergeten?", "Noodstop: schakelaar OFF"]),
         ("Start niet zonder USB", ["Opgeslagen als main.py?", "Batterijen vol?"])]
for k, (h, b) in enumerate(probl):
    cx = 0.8 + (k % 3) * 4.0
    cy = 1.65 + (k // 3) * 2.3
    card(s, cx, cy, 3.8, 2.1, h, ["• " + t for t in b], fill=[RED_T, LILAC_T, BLUE_T][k % 3],
         head_color=RED if k % 3 == 0 else NAVY, size=15)
strip_empty(s)

# ---------------------------------------------------------------- afsluiting
s = new(L_TITLE_ONLY, "Afsluiting: wat kun je nu?",
        "Afsluiting (15:30, ±10 min). Laat 1 of 2 studenten hun patroon of dans demonstreren.\n"
        "Opruimen: schakelaar op OFF. Vooruitblik: in les 4 programmeer je de actoren: motoren, LEDs, buzzer en het display.")
geleerd = ["De Pico-robot bouwen en aansluiten", "Thonny verbinden met de Pico",
           "Een programma opslaan en uitvoeren", "Rijden, draaien en stoppen met pico_car",
           "Veilig testen en problemen oplossen"]
y = 1.75
for g in geleerd:
    circle_num(s, 0.8, y + 0.02, "✓", fill=GREEN, d=0.42, size=14)
    text(s, 1.4, y, 5.0, 0.5, g, size=18, anchor=MSO_ANCHOR.MIDDLE)
    y += 0.7
pill(s, 0.8, 5.55, 5.2, "Schakelaar op OFF bij het opruimen", fill=NAVY)
box(s, 6.9, 1.7, 5.7, 4.5, BLUE_T)
text(s, 7.15, 1.85, 5.2, 0.5, "Volgende week: actoren", size=20, bold=True, color=NAVY)
acts = [("Motoren", "nauwkeuriger rijden"), ("LEDs", "licht en kleur"), ("Buzzer", "geluid en melodietjes"),
        ("OLED-display", "tekst op het scherm")]
y = 2.55
for h, b in acts:
    circle_num(s, 7.15, y, "→", fill=RED, d=0.45, size=14)
    text(s, 7.8, y - 0.05, 4.6, 0.55, [[(h + "  ", {"bold": True}), (b, {})]], size=17, anchor=MSO_ANCHOR.MIDDLE)
    y += 0.8
text(s, 7.15, 5.6, 5.2, 0.4, "Thuis: extra uitdagingen A–D in de handleiding", size=14, italic=True, color=MUTED)
strip_empty(s)

# ---------------------------------------------------------------- eindslide naar achteren
lst = prs.slides._sldIdLst
end = list(lst)[1]
lst.remove(end)
lst.append(end)
prs.slides[len(prs.slides) - 1].notes_slide.notes_text_frame.text = "Vragen? Schakelaar op OFF en de robot veilig opbergen."

prs.save(OUT)
print("saved", OUT, len(prs.slides), "slides")
