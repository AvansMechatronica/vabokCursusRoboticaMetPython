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




# ================================================================ gedeelde blokken (les 4 en verder)
import os as _os, tempfile as _tempfile
from PIL import Image as _Image

URL = "https://avansmechatronica.github.io/vabokCursusRoboticaMetPython/"
_TMP = _tempfile.mkdtemp(prefix="pptx_img_")


def pic(slide, path, x, y, w, h, border=False):
    """Afbeelding passend in kader (x, y, w, h), beeldverhouding behouden.
    Grote foto's worden verkleind (max 1600 px) zodat de pptx klein blijft; GIF's blijven intact (animatie)."""
    im = _Image.open(path)
    iw, ih = im.size
    if not path.lower().endswith(".gif") and max(iw, ih) > 1600:
        f = 1600 / max(iw, ih)
        small = _os.path.join(_TMP, _os.path.basename(path))
        im.convert("RGB").resize((int(iw * f), int(ih * f))).save(small, quality=88)
        path = small
    scale = min(w / iw, h / ih)
    pw, phh = iw * scale, ih * scale
    p = slide.shapes.add_picture(path, Inches(x + (w - pw) / 2), Inches(y + (h - phh) / 2), Inches(pw), Inches(phh))
    if border:
        p.line.color.rgb = RGBColor(0xBB, 0xBB, 0xBB); p.line.width = Pt(0.75)
    return p


def titel(les, notes):
    s = prs.slides[0]
    for p in s.placeholders:
        if p.placeholder_format.idx == 21:
            runs = p.text_frame.paragraphs[0].runs
            runs[0].text = "Les "
            runs[1].text = les
            for r in runs[2:]:
                r.text = ""
    s.notes_slide.notes_text_frame.text = notes


def agenda(items, notes, size=19):
    s = new(L_AGENDA, "Vandaag", notes)
    set_lines(ph(s, 21).text_frame, items, size=size, space_after=12)
    strip_empty(s)
    return s


def website(stappen, notes, img):
    s = new(L_TITLE_ONLY, "Het lesmateriaal: alles staat online", notes + "\nURL: " + URL)
    y = 1.8
    for k, st in enumerate(stappen):
        circle_num(s, 0.8, y, k + 1, d=0.5, size=17)
        text(s, 1.5, y, 4.7, 0.5, st, size=18, anchor=MSO_ANCHOR.MIDDLE)
        y += 0.85
    p_ = pic(s, img, 6.6, 1.6, 6.0, 4.1, border=True)
    p_.click_action.hyperlink.address = URL
    ub = box(s, 0.8, 5.9, 11.8, 0.65, LILAC_T, radius=0.3)
    tf = ub.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = URL.replace("https://", "").rstrip("/")
    r.font.size = Pt(22); r.font.bold = True; r.font.color.rgb = NAVY
    r.hyperlink.address = URL
    strip_empty(s)
    return s


def deel(lay, titel_, sub, notes):
    s = new(lay, titel_, notes)
    set_lines(ph(s, 21).text_frame, [sub], size=22)
    strip_empty(s)
    return s


def pauze(tekst, notes):
    s = new(L_PAUZE, tekst, notes)
    strip_empty(s)
    return s


def checklist(slide, x, y, items, w=5.0, step=0.65, size=18, sym="✓", fill=GREEN):
    for g in items:
        circle_num(slide, x, y + 0.02, sym, fill=fill, d=0.42, size=14)
        text(slide, x + 0.6, y, w, 0.5, g, size=size, anchor=MSO_ANCHOR.MIDDLE)
        y += step
    return y


def kaartgrid(slide, items, cols=3, x0=0.8, y0=1.65, w=3.8, h=2.1, gx=4.0, gy=2.3, size=15):
    fills = [RED_T, LILAC_T, BLUE_T]
    for k, (hd, body) in enumerate(items):
        cx = x0 + (k % cols) * gx
        cy = y0 + (k // cols) * gy
        card(slide, cx, cy, w, h, hd, ["• " + t for t in body], fill=fills[k % 3],
             head_color=RED if k % 3 == 0 else NAVY, size=size)


def uitleg_rijen(slide, x, y, w, rows, rh=0.82, gap=0.1):
    for h_, b in rows:
        box(slide, x, y, w, rh, GREY)
        text(slide, x + 0.2, y + 0.05, w - 0.4, 0.4, h_, size=15, bold=True, color=RED, font="Courier New")
        text(slide, x + 0.2, y + 0.42, w - 0.4, 0.4, b, size=14)
        y += rh + gap
    return y


def afronden(out, notes_eind):
    lst = prs.slides._sldIdLst
    end = list(lst)[1]
    lst.remove(end)
    lst.append(end)
    prs.slides[len(prs.slides) - 1].notes_slide.notes_text_frame.text = notes_eind
    prs.save(out)
    print("saved", out, len(prs.slides), "slides")
