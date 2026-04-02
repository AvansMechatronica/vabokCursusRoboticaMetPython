# Display Code Uitleg


## Wat doet deze code?
Deze code laat tekst en pixels zien op het OLED-display van de Pico. Het toont eerst "Hello", daarna "World" en uiteindelijk een enkele pixel op het scherm.

## Stap-voor-stap uitleg

```python
from machine import Pin, I2C
from pico_car import SSD1306_I2C
import time
```
**Wat gebeurt hier?**
We halen gereedschap uit onze "gereedschapskist":
- `Pin` en `I2C`: om de Pico met het OLED-display te laten praten
- `SSD1306_I2C`: de driver voor het OLED-display
- `time`: voor het wachten tussen stappen

```python
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=100000)
```
**Wat gebeurt hier?**
- We starten I2C-bus 1 op
- `scl=Pin(15)` is de kloklijn, `sda=Pin(14)` is de datalijn
- `freq=100000` betekent 100 kHz communicatiesnelheid

:::{note}
Een I2C-bus is een manier waarop de Pico en het OLED-display met elkaar kunnen praten. De kloklijn (SCL) synchroniseert de communicatie, terwijl de datalijn (SDA) de informatie verzendt.
:::

```python
oled = SSD1306_I2C(128, 32, i2c)
```
**Wat gebeurt hier?**
- We maken een OLED-object van 128x32 pixels
- Vanaf nu sturen we alles naar `oled` om op het scherm te tekenen

```python
oled.text("Hello", 0, 0)
oled.show()
```
**Wat gebeurt hier?**
- `oled.text("Hello", 0, 0)` zet de tekst op positie x=0, y=0
- `oled.show()` ververst het scherm zodat de tekst echt zichtbaar wordt

```python
oled.fill(0)
time.sleep(1)
```
**Wat gebeurt hier?**
- `oled.fill(0)` maakt het scherm leeg (zwart)
- `time.sleep(1)` wacht 1 seconde voordat de volgende afbeelding komt

```python
oled.text("World", 0, 10)
oled.show()
oled.fill(0)
time.sleep(1)
```
**Wat gebeurt hier?**
- Nu tonen we "World" op een iets lagere regel (`y=10`)
- Daarna verversen, wissen en weer 1 seconde wachten

```python
oled.pixel(100, 30, 1)
oled.show()
oled.fill(0)
time.sleep(1)
```
**Wat gebeurt hier?**
- `oled.pixel(100, 30, 1)` zet precies 1 pixel aan op positie x=100, y=30
- Zo kun je heel precies tekenen op het OLED-scherm
- Daarna wordt het scherm opnieuw ververst, gewist en wacht de code 1 seconde

## Hoe werkt een OLED-display?
Een OLED-scherm bestaat uit heel veel kleine lichtpuntjes (pixels). Met code bepaal je welke pixels aan of uit staan. De Pico tekent eerst in het geheugen en met `oled.show()` stuur je het complete beeld naar het scherm.

## Samengevat
De robot laat op het OLED-scherm achter elkaar "Hello", "World" en een losse pixel zien. Tussen elke stap wordt het scherm gewist en 1 seconde gewacht.
