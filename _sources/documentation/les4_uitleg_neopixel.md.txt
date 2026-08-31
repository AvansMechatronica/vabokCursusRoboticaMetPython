# NeoPixel Code Uitleg

## Wat is een NeoPixel?
Een NeoPixel is een klein LED-lampje dat in verschillende kleuren kan oplichten. Op onze robot hebben we een rijtje van 8 NeoPixels die we kunnen programmeren om verschillende kleuren en effecten te laten zien.

## Wat doet deze code?
Deze code laat de NeoPixels op de Pico-robot oplichten in een bewegend patroon. Het is alsof je een lichtshow maakt met de NeoPixels, waarbij de kleuren steeds veranderen en bewegen. Met deze code kun je:
- De NeoPixels in verschillende kleuren laten oplichten
- Bewegende lichteffecten creëren
- Je robot er cool uit laten zien!

## Stap-voor-stap uitleg

### 1. Bibliotheken laden
```python
import time
from pico_car import ws2812b
```
- `time` gebruiken we om korte pauzes te maken.
- `ws2812b` is de module om de NeoPixels te besturen.

### 2. Aantal leds instellen
```python
num_leds = 8
```
- We vertellen de code dat er 8 NeoPixels zijn.

### 3. NeoPixels koppelen aan de juiste pin
```python
pixels = ws2812b(num_leds, 0)
```
- Hier maken we het `pixels` object aan.
- `num_leds` zegt hoeveel leds er zijn.
- `0` is de pin waarop de leds zijn aangesloten.

### 4. Alle leds eerst zacht aanzetten
```python
pixels.fill(10,10,10)
pixels.show()
```
- `fill(10,10,10)` zet alle leds op dezelfde kleur: een zachte wit/grijs tint.
- De drie getallen zijn `rood, groen, blauw` (RGB).
- `show()` stuurt de ingestelde kleur echt naar de leds.

### 5. Oneindige animatie starten
```python
while True:
```
- `while True` betekent: blijf dit voor altijd herhalen.

### 6. Lopend lichteffect maken met twee lussen
```python
for i in range(num_leds):
        for j in range(num_leds):
                pixels.set_pixel(j,abs(i+j)%10,abs(i-(j+3))%10,abs(i-(j+6))%10)
        pixels.show()
        time.sleep(0.05)
```
- De buitenste lus (`i`) bepaalt de fase van de animatie.
- De binnenste lus (`j`) werkt elke led apart bij.
- `set_pixel(j, r, g, b)` stelt led `j` in op kleur `r,g,b`.
- De kleurwaardes worden berekend met formules:
    - `abs(...)` maakt de waarde positief.
    - `%10` houdt de helderheid laag tussen 0 en 9.
- `pixels.show()` laat alle nieuwe kleuren tegelijk zien.
- `time.sleep(0.05)` geeft een korte pauze, zodat je een vloeiende beweging ziet.

### 7. Waarom ziet dit eruit als een bewegend effect?
- Omdat `i` telkens verandert, verschuiven de RGB-waarden bij elke stap.
- Daardoor lijken kleuren over de led-strip te "lopen".
- Met andere getallen in de formules kun je heel andere effecten maken.



## Samengevat
1. **Voorbereiding** — We maken verbinding met de NeoPixels en stellen het aantal in
2. **Kleuren instellen** — We zeggen welke kleuren de NeoPixels moeten hebben
3. **Effecten toevoegen** — We maken een lopend licht effect door de kleuren te veranderen
4. **Afspelen** — We voeren de code uit om de NeoPixels te laten oplichten en bewegen

De robot laat de NeoPixels in een doorlopend kleurpatroon oplichten, zodat je een dynamisch lopend lichteffect krijgt.
