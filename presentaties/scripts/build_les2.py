"""Bouwt presentaties/les2.pptx (les 2a + 2b) op basis van presentaties/template.pptx."""
import copy, sys
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

ROOT = sys.argv[1]
TEMPLATE = ROOT + "/presentaties/template.pptx"
OUT = sys.argv[2]
IMG_ONLINE = ROOT + "/documentation/images/online_python.png"

RED = RGBColor(0xC6, 0x00, 0x2A)
NAVY = RGBColor(0x00, 0x1A, 0x6A)
BLUE = RGBColor(0x00, 0x99, 0xFF)
LILAC = RGBColor(0xDF, 0xBE, 0xFF)
ORANGE = RGBColor(0xFF, 0x52, 0x00)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x1A, 0x1A, 0x1A)
GREY = RGBColor(0xF2, 0xF2, 0xF2)
LILAC_T = RGBColor(0xF4, 0xEA, 0xFF)
BLUE_T = RGBColor(0xE3, 0xF3, 0xFF)
RED_T = RGBColor(0xFB, 0xE6, 0xEA)
GREEN = RGBColor(0x1E, 0x8C, 0x45)
GREEN_T = RGBColor(0xE5, 0xF4, 0xEA)
COMMENT = RGBColor(0x8F, 0xD3, 0xFF)
MUTED = RGBColor(0x55, 0x55, 0x55)

prs = Presentation(TEMPLATE)
M = prs.slide_masters


def layout(m, i):
    return M[m].slide_layouts[i]


L_AGENDA = layout(2, 5)
L_TITLE_ONLY = layout(3, 8)
L_DOEN = layout(4, 0)        # Avatile - Rood
L_DEEL_A = layout(4, 4)      # Avatiles versie 1
L_DEEL_B = layout(4, 5)      # Avatiles versie 2
L_PAUZE = layout(0, 12)      # Titelslide basic blauw


def ph(slide, idx):
    for p in slide.placeholders:
        if p.placeholder_format.idx == idx:
            return p
    raise KeyError(idx)


def strip_empty(slide, keep=()):
    for p in list(slide.placeholders):
        if p.placeholder_format.idx in keep:
            continue
        if not p.has_text_frame or not p.text_frame.text.strip():
            p._element.getparent().remove(p._element)


def new(lay, title, notes=None):
    s = prs.slides.add_slide(lay)
    if title is not None:
        s.shapes.title.text = title
    if notes:
        s.notes_slide.notes_text_frame.text = notes
    return s


def set_lines(tf, lines, size=None, color=None, bold_prefix=True, space_after=6):
    """lines: str of (label, rest) tuples."""
    tf.clear()
    for k, ln in enumerate(lines):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        p.space_after = Pt(space_after)
        parts = ln if isinstance(ln, tuple) else (None, ln)
        if parts[0]:
            r = p.add_run(); r.text = parts[0]; r.font.bold = True
            if size: r.font.size = Pt(size)
            if color: r.font.color.rgb = color
        r = p.add_run(); r.text = parts[1]
        if size: r.font.size = Pt(size)
        if color: r.font.color.rgb = color


def box(slide, x, y, w, h, fill, radius=0.08, name=None):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.adjustments[0] = radius
    sh.fill.solid(); sh.fill.fore_color.rgb = fill
    sh.line.fill.background()
    sh.shadow.inherit = False
    if name: sh.name = name
    return sh


def text(slide, x, y, w, h, runs, size=16, color=BLACK, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, font=None, italic=False, margin=0.0):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(margin)
    tf.vertical_anchor = anchor
    paras = runs if isinstance(runs, list) else [runs]
    for k, para in enumerate(paras):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        p.alignment = align
        segs = para if isinstance(para, list) else [para]
        for seg in segs:
            if isinstance(seg, tuple):
                t, opt = seg
            else:
                t, opt = seg, {}
            r = p.add_run(); r.text = t
            r.font.size = Pt(opt.get("size", size))
            r.font.bold = opt.get("bold", bold)
            r.font.italic = opt.get("italic", italic)
            r.font.color.rgb = opt.get("color", color)
            f = opt.get("font", font)
            if f: r.font.name = f
    return tb


def code(slide, x, y, w, code_str, size=16, h=None, fill=NAVY):
    lines = code_str.strip("\n").split("\n")
    lh = size / 72 * 1.25
    h = h or (len(lines) * lh + 0.4)
    b = box(slide, x, y, w, h, fill, radius=0.05)
    tf = b.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.25)
    tf.margin_top = tf.margin_bottom = Inches(0.18)
    tf.vertical_anchor = MSO_ANCHOR.TOP
    for k, ln in enumerate(lines):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        body, cm = ln, ""
        if "#" in ln and not ln.strip().startswith(("print(\"#", )):
            i = ln.index("#"); body, cm = ln[:i], ln[i:]
        for t, c in ((body, WHITE), (cm, COMMENT)):
            if not t:
                continue
            r = p.add_run(); r.text = t
            r.font.name = "Courier New"; r.font.size = Pt(size); r.font.bold = True
            r.font.color.rgb = c
        if not body and not cm:
            r = p.add_run(); r.text = " "; r.font.size = Pt(size); r.font.name = "Courier New"
    return b, y + h


def card(slide, x, y, w, h, head, body, fill=LILAC_T, head_color=NAVY, size=15, head_size=19):
    box(slide, x, y, w, h, fill)
    text(slide, x + 0.25, y + 0.2, w - 0.5, 0.5, head, size=head_size, bold=True, color=head_color)
    if body:
        text(slide, x + 0.25, y + 0.75, w - 0.5, h - 0.9, body, size=size, color=BLACK)


def pill(slide, x, y, w, label, fill=RED, color=WHITE, size=16, h=0.5):
    b = box(slide, x, y, w, h, fill, radius=0.5)
    tf = b.text_frame
    tf.margin_left = tf.margin_right = Inches(0.15); tf.margin_top = tf.margin_bottom = Inches(0)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = label; r.font.size = Pt(size); r.font.bold = True; r.font.color.rgb = color
    return b


def circle_num(slide, x, y, n, fill=RED, d=0.6, size=20):
    c = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    c.fill.solid(); c.fill.fore_color.rgb = fill; c.line.fill.background(); c.shadow.inherit = False
    tf = c.text_frame; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = str(n); r.font.size = Pt(size); r.font.bold = True; r.font.color.rgb = WHITE


def next_step(slide, label):
    lbl = "Nu jij  →  " + label
    pill(slide, 0.8, 6.35, max(5.2, len(lbl) * 0.13 + 0.8), lbl)


def doen(title, lines, notes, foot=None):
    s = new(L_DOEN, title, notes)
    set_lines(ph(s, 21).text_frame, lines, size=20, space_after=14)
    if foot:
        text(s, 6.9, 6.3, 5.7, 0.5, foot, size=14, italic=True, color=MUTED)
    strip_empty(s, keep=(11,))
    return s


# ---------------------------------------------------------------- 1 titel
title_slide = prs.slides[0]
for p in title_slide.placeholders:
    if p.placeholder_format.idx == 21:
        runs = p.text_frame.paragraphs[0].runs
        runs[0].text = "Les "
        runs[1].text = "2: Introductie in Python programmeren"
title_slide.notes_slide.notes_text_frame.text = (
    "Welkom. Vandaag één lange les in twee delen: 2a (Python basis) en 2b (interactief programmeren).\n"
    "Benadruk: vandaag werk je vooral zelfstandig met de online handleiding; de dia's zijn korte uitleg op het juiste moment.")

# ---------------------------------------------------------------- 2 planning
s = new(L_AGENDA, "Vandaag",
        "Laat deze dia kort zien en wijs op de pauze. De tijden zijn richtlijnen: wie sneller is, gaat gewoon door.")
set_lines(ph(s, 21).text_frame, [
    ("12:30  ", "Introductie en werkwijze"),
    ("12:45  ", "Deel 2a – Python basis (opdracht 1–4)"),
    ("14:00  ", "Pauze"),
    ("14:15  ", "Deel 2b – Interactief programmeren (opdracht 1–4)"),
    ("15:30  ", "Afsluiting en vooruitblik"),
    ("15:45  ", "Einde"),
], size=20, space_after=14)
strip_empty(s)

# ---------------------------------------------------------------- 3 introductie: waar staan we
s = new(L_TITLE_ONLY, "Waar staan we in de cursus?",
        "Introductie (±3 min). Koppel terug aan het bezoek aan Hoppenbouwers: daar zag je robots in de praktijk.\n"
        "Vraag: 'Wie heeft al eens geprogrammeerd?' Handen tellen — geeft je een beeld van de groep.\n"
        "Kernboodschap: een robot doet precies wat jij hem opdraagt. Daarvoor heb je een programmeertaal nodig.")
steps = [("Vorige week", "Bezoek Hoppenbouwers: robots in de praktijk", LILAC_T),
         ("Vandaag", "Leren programmeren in Python", RED_T),
         ("Volgende week", "Je eigen robot bouwen en programmeren", BLUE_T)]
x = 0.8
for k, (h, b, f) in enumerate(steps):
    card(s, x, 1.9, 3.6, 2.2, h, b, fill=f, size=18, head_color=RED if k == 1 else NAVY)
    if k < 2:
        text(s, x + 3.62, 2.6, 0.5, 0.8, "→", size=36, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    x += 4.1
box(s, 0.8, 4.6, 11.8, 1.4, GREY)
text(s, 1.1, 4.6, 11.2, 1.4,
     [[("Een robot doet precies wat jij hem opdraagt — niet meer en niet minder.", {"bold": True, "size": 22, "color": NAVY})],
      [("Een programmeertaal zoals Python is de taal waarin je die opdrachten geeft.", {"size": 18})]],
     anchor=MSO_ANCHOR.MIDDLE)
strip_empty(s)

# ---------------------------------------------------------------- 4 leerdoelen
s = new(L_TITLE_ONLY, "Leerdoelen van vandaag",
        "Noem de twee delen. Deel 2a is de basis, deel 2b maakt je programma's interactief. Alles wat je vandaag leert, gebruik je volgende week op de robot.")
card(s, 0.8, 1.7, 5.7, 4.4, "Deel 2a – Python basis",
     ["• Uitleggen wat een programmeertaal is", "• Code uitvoeren in een online omgeving",
      "• Tekst en getallen printen met print()", "• Werken met variabelen en datatypes",
      "• Rekenen met Python"], fill=LILAC_T, size=20)
card(s, 6.9, 1.7, 5.7, 4.4, "Deel 2b – Interactief programmeren",
     ["• Invoer vragen met input()", "• Keuzes maken met if / elif / else",
      "• Code herhalen met for- en while-loops", "• Een eigen interactief programma maken"],
     fill=BLUE_T, size=20)
strip_empty(s)

# ---------------------------------------------------------------- 5 werkwijze
s = new(L_TITLE_ONLY, "Zo werken we vandaag",
        "Belangrijkste dia van de introductie. Op het HBO wordt verwacht dat je zelf informatie zoekt en uitprobeert.\n"
        "Leg de regel uit: eerst 5 minuten zelf proberen, dan je buur, dan de docent.\n"
        "Vertel dat je af en toe de groep even stilzet voor een korte uitleg (max. 5 min) als veel mensen bij een nieuw onderwerp zijn.")
items = [("Lees de handleiding", "Alle uitleg en opdrachten staan in het online lesmateriaal: les 2a en les 2b."),
         ("Probeer en test", "Typ de code zelf over, druk op Run en kijk wat er gebeurt. Fouten maken mag!"),
         ("Vastgelopen?", "Eerst 5 minuten zelf → dan je buur → dan de docent."),
         ("Korte uitleg", "Bij een nieuw onderwerp leg ik het kort uit, precies op het moment dat je het nodig hebt.")]
text(s, 0.8, 1.35, 11.8, 0.4, "Zelfstandig werken, net als op het HBO", size=18, italic=True, color=MUTED)
y = 1.95
for k, (h, b) in enumerate(items):
    circle_num(s, 0.8, y + 0.12, k + 1, fill=RED if k < 3 else NAVY)
    text(s, 1.65, y, 10.8, 0.45, h, size=20, bold=True, color=NAVY)
    text(s, 1.65, y + 0.45, 10.8, 0.5, b, size=17)
    y += 1.1
strip_empty(s)

# ---------------------------------------------------------------- lesmateriaal online
URL = "https://avansmechatronica.github.io/vabokCursusRoboticaMetPython/"
IMG_SITE = sys.argv[3]
s = new(L_TITLE_ONLY, "Het lesmateriaal: alle opdrachten online",
        "Laat de website live zien en vraag iedereen hem nu te openen en als bladwijzer op te slaan.\n"
        "Wijs op het menu links: daar staan les 2a en les 2b met alle uitleg en opdrachten.\n"
        "URL: " + URL)
stappen = ["Open de website (link hieronder)", "Kies in het menu links Les 2a of Les 2b",
           "Werk de opdrachten op volgorde door", "Sla de pagina op als bladwijzer"]
y = 1.8
for k, st in enumerate(stappen):
    circle_num(s, 0.8, y, k + 1, d=0.5, size=17)
    text(s, 1.5, y, 4.7, 0.5, st, size=18, anchor=MSO_ANCHOR.MIDDLE)
    y += 0.85
site_w = 6.0
site_h = site_w * 967 / 1432
pic = s.shapes.add_picture(IMG_SITE, Inches(12.6 - site_w), Inches(1.6), Inches(site_w), Inches(site_h))
pic.line.color.rgb = RGBColor(0xBB, 0xBB, 0xBB); pic.line.width = Pt(0.75)
pic.click_action.hyperlink.address = URL
ub = box(s, 0.8, 5.9, 11.8, 0.65, LILAC_T, radius=0.3)
tf = ub.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left = tf.margin_right = Inches(0.2)
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = URL.replace("https://", "").rstrip("/")
r.font.size = Pt(22); r.font.bold = True; r.font.color.rgb = NAVY
r.hyperlink.address = URL
strip_empty(s)

# ================================================================ DEEL 2A
s = new(L_DEEL_A, "Deel 2a",
        "Start deel 2a (12:45). Iedereen opent het lesmateriaal van les 2a en online-python.com.")
set_lines(ph(s, 21).text_frame, ["Python basis: print, variabelen, datatypes en rekenen"], size=22)
strip_empty(s)

# ---------------------------------------------------------------- je eerste programma
s = new(L_TITLE_ONLY, "Je eerste programma",
        "Live demo (±5 min): open online-python.com, maak main.py leeg, typ print(\"Hello, World!\") en klik op Run.\n"
        "Leg uit: print() is een functie, tussen de haakjes staat wat je wilt laten zien, aanhalingstekens = tekst.\n"
        "Laat daarna iedereen hetzelfde doen voordat ze aan opdracht 1 beginnen.")
text(s, 0.8, 1.7, 5.9, 0.5, "Stap voor stap", size=20, bold=True, color=NAVY)
stappen = [[[("Ga naar ", {}), ("online-python.com", {"bold": True})]], "Maak het scherm main.py helemaal leeg",
           "Typ de code hieronder", "Klik op Run (of Ctrl+Enter)"]
y = 2.3
for k, st in enumerate(stappen):
    circle_num(s, 0.8, y, k + 1, d=0.45, size=16)
    text(s, 1.45, y, 5.2, 0.45, st, size=17, anchor=MSO_ANCHOR.MIDDLE)
    y += 0.6
_, y2 = code(s, 0.8, 4.85, 5.9, 'print("Hello, World!")', size=20)
text(s, 0.8, y2 + 0.15, 5.9, 0.5, [[("Uitvoer:  ", {"bold": True}), ("Hello, World!", {"font": "Courier New", "bold": True})]], size=17)
img_h = 4.6
img_w = img_h * 968 / 795
s.shapes.add_picture(IMG_ONLINE, Inches(12.6 - img_w), Inches(1.7), Inches(img_w), Inches(img_h))
strip_empty(s)

doen("Aan de slag: opdracht 1", [
    ("1.1  ", "Print je eigen naam"),
    ("1.2  ", "Print meerdere regels onder elkaar"),
    ("1.3  ", "Print getallen"),
    ("Onderzoek: ", "wat is het verschil tussen print(\"42\") en print(42)?"),
], "Opdracht 1 (±10 min). Loop rond. Bespreek de onderzoeksvraag pas bij het volgende uitlegmoment (datatypes).",
    foot="Lesmateriaal: les 2a, opdracht 1")

# ---------------------------------------------------------------- variabelen
s = new(L_TITLE_ONLY, "Variabelen: een doosje met een naam",
        "Just-in-time uitleg (±4 min) wanneer de meesten klaar zijn met opdracht 1.\n"
        "Metafoor: een variabele is een doosje met een etiket. Je stopt er een waarde in en haalt hem later terug via de naam.\n"
        "Checkvraag: 'Mag mijn naam als variabelenaam? En mijn naam met een spatie?'")
# doosjes
for k, (lbl, val) in enumerate((("naam", '"Jan"'), ("leeftijd", "18"))):
    bx = 0.8 + k * 3.0
    box(s, bx, 1.8, 2.6, 1.6, LILAC, radius=0.12)
    pill(s, bx + 0.3, 1.55, 2.0, lbl, fill=NAVY, size=16, h=0.45)
    text(s, bx, 2.15, 2.6, 1.1, val, size=28, bold=True, color=NAVY, align=PP_ALIGN.CENTER,
         anchor=MSO_ANCHOR.MIDDLE, font="Courier New")
code(s, 0.8, 3.8, 5.6, 'naam = "Jan"\nleeftijd = 18\nprint(naam)\nprint(leeftijd)', size=18)
card(s, 6.9, 1.7, 2.75, 4.4, "Mag wel", ["naam", "Leeftijd", "naam1", "mijn_naam"], fill=GREEN_T,
     head_color=GREEN, size=18)
card(s, 9.85, 1.7, 2.75, 4.4, "Mag niet", [[("1naam", {"bold": True})], "begint met cijfer", [("mijn naam", {"bold": True})], "bevat een spatie", [("naam!", {"bold": True})], "speciaal teken"],
     fill=RED_T, head_color=RED, size=16)
next_step(s, "opdracht 2: werken met variabelen")
strip_empty(s)

doen("Aan de slag: opdracht 2", [
    ("2.1  ", "Maak variabelen over jezelf: naam, leeftijd, woonplaats"),
    ("2.2  ", "Combineer tekst en een variabele met +"),
    ("2.3  ", "Laat Python twee getallen optellen"),
], "Opdracht 2 (±10 min). Let op typische fout: + tussen tekst en een getal geeft een TypeError — goed moment voor een individuele hint.",
    foot="Lesmateriaal: les 2a, opdracht 2")

# ---------------------------------------------------------------- datatypes
s = new(L_TITLE_ONLY, "Datatypes: welke soort gegevens?",
        "Just-in-time uitleg (±4 min). Bespreek nu de onderzoeksvraag van opdracht 1: \"42\" is tekst (string), 42 is een getal (integer).\n"
        "Wijs op de valkuil: kommagetallen schrijf je met een PUNT.\n"
        "Checkvraag: 'Welk datatype is 3.14? En \"3.14\"?'")
types = [("Tekst", "str", '"Sarah"', "tussen aanhalingstekens", LILAC_T),
         ("Geheel getal", "int", "20", "zonder komma", BLUE_T),
         ("Kommagetal", "float", "19.99", "met een punt, niet een komma!", RED_T),
         ("Waar / onwaar", "bool", "True", "alleen True of False", GREEN_T)]
x = 0.8
for h, t, ex, uitleg, f in types:
    box(s, x, 1.7, 2.8, 3.3, f)
    text(s, x + 0.25, 1.9, 2.3, 0.45, h, size=19, bold=True, color=NAVY)
    text(s, x + 0.25, 2.35, 2.3, 0.4, t, size=16, color=MUTED, font="Courier New", bold=True)
    text(s, x + 0.25, 2.95, 2.3, 0.8, ex, size=30, bold=True, color=NAVY, font="Courier New")
    text(s, x + 0.25, 3.95, 2.3, 0.9, uitleg, size=15)
    x += 3.0
box(s, 0.8, 5.25, 11.8, 0.85, GREY)
text(s, 1.05, 5.25, 11.3, 0.85,
     [[("Onthoud:  ", {"bold": True, "color": RED}), ('print("42")', {"font": "Courier New", "bold": True}),
       (" is tekst, ", {}), ("print(42)", {"font": "Courier New", "bold": True}), (" is een getal waarmee je kunt rekenen.", {})]],
     size=18, anchor=MSO_ANCHOR.MIDDLE)
next_step(s, "opdracht 3: datatypes")
strip_empty(s)

doen("Aan de slag: opdracht 3", [
    ("3.1  ", "Bepaal van vier variabelen welk datatype ze hebben"),
    ("3.2  ", "Maak zelf een string, integer, float en boolean"),
    ("Tip: ", "controleer je antwoord met print(type(a))"),
], "Opdracht 3 (±8 min). De tip met type() staat niet in de handleiding; noem hem als verrijking.",
    foot="Lesmateriaal: les 2a, opdracht 3")

# ---------------------------------------------------------------- rekenen
s = new(L_TITLE_ONLY, "Rekenen met Python",
        "Just-in-time uitleg (±4 min). De eerste vijf operatoren kennen ze van de rekenmachine.\n"
        "Besteed de tijd aan // en %: met 17 snoepjes verdeeld over 5 personen krijgt ieder er 3 (//) en blijven er 2 over (%).\n"
        "Modulo komt terug in 2b (even/oneven, FizzBuzz).")
ops = [("+", "optellen", "5 + 3", "8"), ("-", "aftrekken", "10 - 4", "6"),
       ("*", "vermenigvuldigen", "6 * 7", "42"), ("/", "delen", "15 / 3", "5.0"),
       ("**", "tot de macht", "2 ** 3", "8")]
y = 1.7
for op, naam, ex, res in ops:
    box(s, 0.8, y, 6.0, 0.7, GREY)
    text(s, 1.0, y, 0.8, 0.7, op, size=22, bold=True, color=RED, font="Courier New", anchor=MSO_ANCHOR.MIDDLE)
    text(s, 1.8, y, 2.4, 0.7, naam, size=17, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 4.2, y, 2.5, 0.7, [[(ex, {"font": "Courier New", "bold": True}), ("  →  " + res, {"color": NAVY, "bold": True})]],
         size=17, anchor=MSO_ANCHOR.MIDDLE)
    y += 0.85
card(s, 7.2, 1.7, 5.4, 1.95, "//  gehele deling", [[("17 // 5", {"font": "Courier New", "bold": True}),
                                                     ("  →  3", {"bold": True, "color": NAVY})],
                                                    "Hoe vaak past 5 in 17?"], fill=BLUE_T, size=18)
card(s, 7.2, 3.85, 5.4, 1.95, "%  modulo (rest)", [[("17 % 5", {"font": "Courier New", "bold": True}),
                                                     ("  →  2", {"bold": True, "color": NAVY})],
                                                    "Wat blijft er over? 17 = 3 × 5 + 2"], fill=RED_T, size=18)
next_step(s, "opdracht 4: rekenopgaven")
strip_empty(s)

doen("Aan de slag: opdracht 4", [
    ("4.1  ", "Oppervlakte van een rechthoek"),
    ("4.2  ", "Bereken je geboortejaar"),
    ("4.3  ", "Gemiddelde van drie cijfers"),
    ("Klaar? ", "Extra oefeningen A, B en C (o.a. seconden in een week)"),
], "Opdracht 4 (±12 min). Valkuil bij 4.3: (a + b + c) / 3 — zonder haakjes klopt het niet. Laat ze dat zelf ontdekken.",
    foot="Lesmateriaal: les 2a, opdracht 4 en extra oefeningen")

# ---------------------------------------------------------------- hulpkaart 2a
s = new(L_TITLE_ONLY, "Hulpkaart: het werkt niet, wat nu?",
        "Deze dia kan blijven staan terwijl studenten werken. Verwijs ernaar als iemand om hulp vraagt: 'Wat zegt de foutmelding? Kijk eerst op de hulpkaart.'\n"
        "Foutmeldingen lezen is een belangrijke vaardigheid: de laatste regel van de melding vertelt meestal wat er mis is.")
hulp = [("SyntaxError", ["Aanhalingstekens vergeten?  \"tekst\"", "Haakjes compleet?  print(...)", "print met kleine letter, niet Print"], RED_T, RED),
        ("NameError", ["Variabele bestaat (nog) niet", "Check de spelling van de naam", "Eerst maken, dan gebruiken"], LILAC_T, NAVY),
        ("Er gebeurt niets", ["Heb je op Run geklikt?", "Staat er wel code in de editor?"], BLUE_T, NAVY),
        ("Verkeerde uitvoer", ["Lees je code regel voor regel na", "Precies overgetypt?", "Klopt je berekening?"], GREY, NAVY)]
for k, (h, b, f, hc) in enumerate(hulp):
    cx = 0.8 + (k % 2) * 6.1
    cy = 1.7 + (k // 2) * 2.35
    card(s, cx, cy, 5.7, 2.15, h, ["• " + t for t in b], fill=f, head_color=hc, size=16)
strip_empty(s)

# ---------------------------------------------------------------- pauze
s = new(L_PAUZE, "Pauze\n14:15 verder met deel 2b",
        "Pauze (14:00–14:15). Wie deel 2a nog niet af heeft, kan na de pauze kort afronden, maar start daarna met 2b: de opdrachten van 2a zijn de basis, de extra oefeningen zijn voor thuis.")
strip_empty(s)

# ================================================================ DEEL 2B
s = new(L_DEEL_B, "Deel 2b",
        "Start deel 2b (14:15). Iedereen opent het lesmateriaal van les 2b.")
set_lines(ph(s, 21).text_frame, ["Interactief programmeren: input, keuzes en herhalen"], size=22)
strip_empty(s)

# ---------------------------------------------------------------- terugblik quiz
s = new(L_TITLE_ONLY, "Opwarmer: wat print dit?",
        "Terugblik op 2a (±3 min). Laat studenten eerst zelf/in tweetallen voorspellen, dan pas uitvoeren.\n"
        "Antwoorden: 1) 2.5   2) Hoi Ali   3) 34  (tekst + tekst plakt aan elkaar!)\n"
        "Vraag 3 is de opstap naar input(): dat geeft altijd tekst terug.")
qs = ['print(10 / 4)', 'naam = "Ali"\nprint("Hoi " + naam)', 'print("3" + "4")']
x = 0.8
for k, q in enumerate(qs):
    circle_num(s, x, 1.75, k + 1, fill=RED)
    code(s, x, 2.55, 3.7, q, size=18, h=1.5)
    box(s, x, 4.3, 3.7, 1.1, GREY)
    text(s, x + 0.2, 4.3, 3.3, 1.1, "Jouw voorspelling: …", size=17, color=MUTED, italic=True, anchor=MSO_ANCHOR.MIDDLE)
    x += 4.05
text(s, 0.8, 5.75, 11.8, 0.5, "Eerst voorspellen, dan pas uitvoeren!", size=18, bold=True, color=NAVY)
strip_empty(s)

# ---------------------------------------------------------------- robot-brug
s = new(L_TITLE_ONLY, "Van programma naar robot",
        "Koppeling naar de rest van de cursus (±2 min). Wat je in 2b leert, is precies hoe een robot werkt:\n"
        "hij leest een sensor (input), neemt een beslissing (if) en doet dat steeds opnieuw (loop).")
cols = [("Invoer", "input()", "De robot leest een sensor: hoe ver is de muur?", LILAC_T),
        ("Beslissen", "if / else", "Is de muur dichtbij? Dan draaien, anders vooruit.", RED_T),
        ("Herhalen", "while / for", "Blijf dit steeds opnieuw doen.", BLUE_T)]
x = 0.8
for k, (h, c, b, f) in enumerate(cols):
    box(s, x, 1.8, 3.6, 3.6, f)
    circle_num(s, x + 0.3, 2.05, k + 1, fill=NAVY)
    text(s, x + 1.05, 2.05, 2.4, 0.6, h, size=22, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + 0.3, 2.9, 3.0, 0.5, c, size=20, bold=True, color=RED, font="Courier New")
    text(s, x + 0.3, 3.55, 3.0, 1.7, b, size=17)
    if k < 2:
        text(s, x + 3.62, 3.1, 0.5, 0.8, "→", size=36, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    x += 4.1
text(s, 0.8, 5.7, 11.8, 0.5, "Vandaag oefen je dit op de computer, volgende week op de robot.", size=18, italic=True, color=MUTED)
strip_empty(s)

# ---------------------------------------------------------------- input
s = new(L_TITLE_ONLY, "input(): vraag iets aan de gebruiker",
        "Just-in-time uitleg (±4 min). Demonstreer eerst het fout-voorbeeld rechtsboven: leeftijd + 1 geeft een TypeError.\n"
        "Laat dan zien dat int() het oplost. Checkvraag: 'Wat gebruik je voor een prijs als 2.50?' → float().")
_, y2 = code(s, 0.8, 1.7, 6.2, 'naam = input("Wat is je naam? ")\nprint("Hallo " + naam + "!")', size=17)
text(s, 0.8, y2 + 0.2, 6.2, 1.3, ["Het programma wacht tot de gebruiker iets typt en op Enter drukt.",
                                  "Wat getypt wordt, komt in de variabele naam."], size=16)
card(s, 7.4, 1.7, 5.2, 2.3, "Let op: input() geeft altijd tekst", [
    [("input() → ", {}), ('"18"', {"font": "Courier New", "bold": True}), ("  (geen 18)", {})],
    "Rekenen? Eerst omzetten!"], fill=RED_T, head_color=RED, size=17, head_size=18)
code(s, 7.4, 4.2, 5.2, 'leeftijd = int(input("Leeftijd? "))\nprint(leeftijd + 1)', size=15)
text(s, 0.8, 4.2, 6.2, 1.2, [[("int()", {"font": "Courier New", "bold": True, "color": RED}), ("  geheel getal     ", {}),
                              ("float()", {"font": "Courier New", "bold": True, "color": RED}), ("  kommagetal", {})],
                             [("str()", {"font": "Courier New", "bold": True, "color": RED}), ("  terug naar tekst", {})]], size=17)
next_step(s, "opdracht 1: werken met input")
strip_empty(s)

doen("Aan de slag: opdracht 1", [
    ("1.1  ", "Vraag naam en leeftijd en print een begroeting"),
    ("1.2  ", "Maak een rekenmachine die twee getallen optelt"),
    ("1.3  ", "Vraag favoriet eten en kleur, print een leuke zin"),
], "Opdracht 2b-1 (±10 min). Bij 1.1 komt str(leeftijd) voor: vraag waarom dat nodig is.",
    foot="Lesmateriaal: les 2b, opdracht 1")

# ---------------------------------------------------------------- if
s = new(L_TITLE_ONLY, "Keuzes maken met if / elif / else",
        "Just-in-time uitleg (±5 min). Drie aandachtspunten: de dubbele punt, het inspringen (4 spaties) en = versus ==.\n"
        "Loop het voorbeeld door met cijfer 7.2: welke regel wordt geprint? Python stopt bij de eerste voorwaarde die waar is.\n"
        "Noem and / or / not kort; die staan uitgewerkt in de handleiding.")
code(s, 0.8, 1.7, 6.3, 'cijfer = float(input("Cijfer? "))\n\nif cijfer >= 8.0:\n    print("Uitstekend!")\nelif cijfer >= 5.5:\n    print("Voldoende.")\nelse:\n    print("Onvoldoende.")', size=17)
text(s, 0.8, 5.0, 6.3, 1.2, [[("Dubbele punt ", {"bold": True, "color": RED}), (":", {"font": "Courier New", "bold": True}),
                              (" aan het eind van de regel", {})],
                             [("Inspringen ", {"bold": True, "color": RED}), ("(4 spaties) bepaalt wat bij de if hoort", {})]], size=16)
ops = [("==", "gelijk aan"), ("!=", "niet gelijk aan"), (">  <", "groter / kleiner dan"), (">=  <=", "groter / kleiner of gelijk")]
box(s, 7.5, 1.7, 5.1, 2.75, GREY)
y = 1.85
for o, b in ops:
    text(s, 7.75, y, 1.5, 0.55, o, size=18, bold=True, color=NAVY, font="Courier New", anchor=MSO_ANCHOR.MIDDLE)
    text(s, 9.3, y, 3.2, 0.55, b, size=16, anchor=MSO_ANCHOR.MIDDLE)
    y += 0.62
card(s, 7.5, 4.65, 5.1, 1.5, "=  is niet  ==", [[("x = 5", {"font": "Courier New", "bold": True}), ("  geeft x een waarde", {})],
                                               [("x == 5", {"font": "Courier New", "bold": True}), ("  vergelijkt", {})]],
     fill=RED_T, head_color=RED, size=15, head_size=17)
next_step(s, "opdracht 2: if-statements")
strip_empty(s)

doen("Aan de slag: opdracht 2", [
    ("2.1  ", "Is een getal positief, negatief of nul?"),
    ("2.2  ", "Wachtwoord-checker"),
    ("2.3  ", "Mag iemand stemmen? (gebruik and)"),
    ("2.4  ", "Een eenvoudig drankenmenu"),
], "Opdracht 2b-2 (±12 min). Bij 2.4: let op dat keuze tekst is, dus vergelijken met \"1\" en niet met 1.",
    foot="Lesmateriaal: les 2b, opdracht 2")

# ---------------------------------------------------------------- loops
s = new(L_TITLE_ONLY, "Herhalen: for of while?",
        "Just-in-time uitleg (±5 min). Vuistregel: weet je vooraf hoe vaak? → for. Herhalen tot iets gebeurt? → while.\n"
        "range(5) begint bij 0 en stopt vóór 5. Laat studenten voorspellen wat range(1, 6) geeft.\n"
        "Waarschuw voor de oneindige loop en vertel hoe je stopt (Stop-knop in online-python).")
text(s, 0.8, 1.7, 5.7, 0.5, "for: vast aantal keer", size=20, bold=True, color=NAVY)
_, yf = code(s, 0.8, 2.25, 5.7, 'for i in range(1, 6):\n    print("5 x", i, "=", 5 * i)', size=16)
text(s, 0.8, yf + 0.2, 5.7, 1.4, [[("range(5)", {"font": "Courier New", "bold": True}), ("        0, 1, 2, 3, 4", {})],
                                  [("range(1, 6)", {"font": "Courier New", "bold": True}), ("     1, 2, 3, 4, 5", {})],
                                  [("range(0, 10, 2)", {"font": "Courier New", "bold": True}), (" 0, 2, 4, 6, 8", {})]], size=16)
text(s, 6.9, 1.7, 5.7, 0.5, "while: zolang iets waar is", size=20, bold=True, color=NAVY)
_, yw = code(s, 6.9, 2.25, 5.7, 'teller = 0\nwhile teller < 5:\n    print(teller)\n    teller = teller + 1', size=16)
card(s, 6.9, yw + 0.2, 5.7, 1.25, "Pas op: oneindige loop", ["Vergeet je teller = teller + 1, dan stopt het nooit."],
     fill=RED_T, head_color=RED, size=15, head_size=17)
next_step(s, "opdracht 3: werken met loops")
strip_empty(s)

doen("Aan de slag: opdracht 3", [
    ("3.1 – 3.4  ", "Tellen, even getallen, tafel van 7, stappen van 10"),
    ("3.5  ", "Raadspel met een while-loop"),
    ("3.6  ", "Aftellen van 10 naar 0"),
], "Opdracht 2b-3 (±15 min). Hint bij 3.6: range(10, -1, -1). Wie snel klaar is: lees alvast break en continue in de handleiding.",
    foot="Lesmateriaal: les 2b, opdracht 3")

# ---------------------------------------------------------------- break/continue + keuze
s = new(L_TITLE_ONLY, "break en continue",
        "Korte uitleg (±3 min), alleen als de groep eraan toe is; anders laten lezen in de handleiding.\n"
        "break gebruik je straks in de rekenmachine (optie B) om het menu te stoppen.")
text(s, 0.8, 1.7, 5.7, 0.5, "break: stop de loop", size=20, bold=True, color=NAVY)
code(s, 0.8, 2.25, 5.7, 'for i in range(10):\n    if i == 5:\n        break\n    print(i)\n# 0 1 2 3 4', size=16)
text(s, 6.9, 1.7, 5.7, 0.5, "continue: sla deze ronde over", size=20, bold=True, color=NAVY)
code(s, 6.9, 2.25, 5.7, 'for i in range(10):\n    if i == 5:\n        continue\n    print(i)\n# 0 1 2 3 4 6 7 8 9', size=16)
card(s, 0.8, 4.6, 11.8, 1.3, "Waar gebruik je dit?", ["In de rekenmachine (optie B) stopt break het menu als de gebruiker kiest voor Stop."], fill=BLUE_T, size=17)
next_step(s, "opdracht 4: eigen programma")
strip_empty(s)

doen("Aan de slag: opdracht 4", [
    ("Kies je eigen programma:", ""),
    ("A  Quiz  ", "– stel vragen en houd de score bij"),
    ("B  Rekenmachine  ", "– een menu dat blijft draaien"),
    ("C  Raadspel  ", "– met hints: te hoog of te laag"),
    ("Daarna: ", "breid uit met meer vragen, opties of foutafhandeling"),
], "Opdracht 2b-4 (tot ±15:30). Hier komt alles samen. Stimuleer uitbreiden: dat is het verschil tussen overtypen en echt programmeren.\n"
   "Laat 1 of 2 studenten aan het eind kort hun programma laten zien.",
    foot="Lesmateriaal: les 2b, opdracht 4")

# ---------------------------------------------------------------- hulpkaart 2b
s = new(L_TITLE_ONLY, "Hulpkaart: veelgemaakte fouten",
        "Kan blijven staan tijdens opdracht 3 en 4. Deze vier fouten zie je het meest.")
fouten = [("Input niet omgezet", 'leeftijd = input("Leeftijd? ")', 'leeftijd = int(input("Leeftijd? "))'),
          ("Inspringen vergeten", 'if leeftijd >= 18:\nprint("Volwassen")', 'if leeftijd >= 18:\n    print("Volwassen")'),
          ("= in plaats van ==", "if x = 5:", "if x == 5:"),
          ("Oneindige loop", "while teller < 10:\n    print(teller)", "while teller < 10:\n    print(teller)\n    teller = teller + 1")]
for k, (h, fout, goed) in enumerate(fouten):
    cx = 0.8 + (k % 2) * 6.1
    cy = 1.65 + (k // 2) * 2.45
    box(s, cx, cy, 5.7, 2.3, GREY)
    text(s, cx + 0.2, cy + 0.1, 5.3, 0.4, h, size=17, bold=True, color=NAVY)
    text(s, cx + 0.2, cy + 0.55, 0.9, 0.4, "Fout", size=13, bold=True, color=RED)
    code(s, cx + 1.0, cy + 0.55, 4.5, fout, size=13, fill=RED, h=0.75)
    text(s, cx + 0.2, cy + 1.4, 0.9, 0.4, "Goed", size=13, bold=True, color=GREEN)
    code(s, cx + 1.0, cy + 1.4, 4.5, goed, size=13, fill=GREEN, h=0.8)
strip_empty(s)

# ---------------------------------------------------------------- afsluiting
s = new(L_TITLE_ONLY, "Afsluiting: wat kun je nu?",
        "Afsluiting (15:30, ±10 min). Laat studenten per onderwerp zelf inschatten: lukt het (duim omhoog) of nog lastig?\n"
        "Vooruitblik: volgende week bouw je de robot en gebruik je precies deze bouwstenen. De code rechts is een schets (pseudocode), niet de echte robotcode.\n"
        "Extra oefeningen 2a (A–C) en 2b (A–E) zijn voor thuis.")
geleerd = ["print() en variabelen", "Datatypes: str, int, float, bool", "Rekenen, ook met // en %",
           "input() met int() en float()", "Keuzes met if / elif / else", "Herhalen met for en while"]
y = 1.75
for g in geleerd:
    circle_num(s, 0.8, y + 0.02, "✓", fill=GREEN, d=0.42, size=14)
    text(s, 1.4, y, 5.0, 0.5, g, size=18, anchor=MSO_ANCHOR.MIDDLE)
    y += 0.65
text(s, 0.8, 5.8, 5.6, 0.5, "Thuis: extra oefeningen in de handleiding", size=16, italic=True, color=MUTED)
box(s, 6.9, 1.7, 5.7, 4.5, BLUE_T)
text(s, 7.15, 1.85, 5.2, 0.5, "Volgende week: je eerste robot", size=19, bold=True, color=NAVY)
code(s, 7.15, 2.5, 5.2, 'while True:\n    afstand = meet_afstand()\n    if afstand < 20:\n        draai()\n    else:\n        rijd_vooruit()', size=15)
text(s, 7.15, 5.5, 5.2, 0.5, "Schets – de echte code volgt in les 3", size=13, italic=True, color=MUTED)
strip_empty(s)

# ---------------------------------------------------------------- eindslide naar achteren
lst = prs.slides._sldIdLst
ids = list(lst)
end = ids[1]
lst.remove(end)
lst.append(end)
prs.slides[len(prs.slides) - 1].notes_slide.notes_text_frame.text = "Vragen? Ruim de laptops op en zorg dat je volgende week het lesmateriaal van les 3 kunt openen."

prs.save(OUT)
print("saved", OUT, len(prs.slides), "slides")
