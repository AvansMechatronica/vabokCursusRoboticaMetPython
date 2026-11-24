# Presentaties genereren

De presentaties in `presentaties/` worden gemaakt met Python (python-pptx) op basis van
`presentaties/template.pptx` (Avans/Yonder-huisstijl). Dit document is ook de overdracht
voor wie (of welke Claude-sessie) hier verder aan werkt.

## Bestanden

| Bestand | Doel |
|---|---|
| `helpers.py` | Gedeelde code: template laden, layouts, kaarten, codeblokken, pills |
| `build_les2.py` | Maakt `les2.pptx` (les 2a + 2b in één presentatie) |
| `build_les3.py` | Maakt `les3.pptx` (bouwen → controle → Pico → programmeren); gebruikt `helpers.py` |
| `build_les4.py` | Maakt `les4.pptx` (actoren: motoren, LED, display, buzzer, functies, NeoPixels) |
| `build_les5.py` | Maakt `les5.pptx` (sensoren: licht, ultrasoon, tracking; meten → beslissen → doen) |
| `website.png` | Screenshot van de GitHub Pages-site voor de dia "Het lesmateriaal" |
| `render.ps1` | Exporteert dia's als PNG via PowerPoint (om te controleren) |
| `pptx2pdf.ps1` | Exporteert een presentatie naar PDF via PowerPoint |
| `docx2pdf.ps1` | Exporteert een Word-document naar PDF via Word |

## Gebruik (Windows, PowerShell, vanuit de hoofdmap van de repo)

```powershell
pip install python-pptx pillow
python presentaties/scripts/build_les3.py . presentaties/les3_nieuw.pptx presentaties/scripts/website.png
powershell -ExecutionPolicy Bypass -File presentaties/scripts/render.ps1 "$PWD\presentaties\les3_nieuw.pptx" "$PWD\render"
```

Schrijf eerst naar een nieuw bestand en vergelijk; overschrijf `lesN.pptx` pas daarna.
Handmatige aanpassingen in PowerPoint gaan verloren als je opnieuw genereert: neem ze eerst over in het script.

## Afspraken / ontwerpkeuzes

- Elke les begint met een korte introductie: planning ("Vandaag"), terugblik, leerdoelen, werkwijze, link naar het lesmateriaal.
- Nadruk op zelfstandig werken; uitleg is kort en "just in time".
- **Witte dia's** = korte uitleg, eindigen met een rode knop "Nu jij → opdracht X".
- **Rode dia's** (layout *Avatile - Rood*) = "Aan de slag", kunnen blijven staan tijdens het werken.
- Hulpkaart met veelgemaakte fouten per les; sprekersnotities met timing en controlevragen.
- Bibliotheek heet `pico_car` (kleine letters): `from pico_car import pico_car`.
- Les 3: studenten tekenen eerst `support/uitleenovereenkomst.docx`, bouwen, laten de robot controleren
  door de docent en krijgen dan pas de geprogrammeerde Raspberry Pi Pico.

## PDF's en GitHub Pages

PDF's van de presentaties staan in `presentaties/` én in `documentation/presentaties/`.
Alleen die laatste map komt op de website (Sphinx bouwt vanuit `documentation/`).
De lessen linken ernaar met:

```markdown
:::{note}
De presentatie van deze les: {download}`Les 2 – presentatie (PDF) <../presentaties/les2.pdf>`
:::
```

## Status (24 november 2026)

- Klaar: les 2 t/m 5. Lestijden 12:30–15:45 (pauze 14:00–14:15).
- PDF's van les 2 en 3 gekoppeld in de handleiding; les 4 en 5 nog niet.
- `les4 .pptx` (met spatie) is de oude lege versie; de nieuwe heet `les4.pptx`.
- Nog te doen: les 6 (eigen robot-werktuig) e.v.
