# Buzzer Code Uitleg

## Wat is een Buzzer?
Een buzzer is een klein elektronisch apparaatje dat geluid kan maken. Op onze robot geniet de buzzer ervan om verschillende tonen af te spelen — hoge tonen, lage tonen, snel, langzaam. Het is als een kleine luidspreker!

## Wat doet deze code?
Deze code laat de buzzer op de Pico geluid maken. Het is zoals een klein muziekinstrument dat verschillende tonen kan afspelen — precies volgens de opgegeven frequenties en duur. Met deze code kun je:
- Verschillende tonen afspelen
- Muziek componeren
- Signalen maken (piep, geluid)

## Stap-voor-stap uitleg
```python
from machine import Pin, PWM
import time
```
**Wat gebeurt hier?**
- `from machine import Pin, PWM` — We halen twee gereedschappen, Pin en PWM. Pin is om contact te maken met de buzzer. PWM is om de buzzer met verschillende sterkte aan en uit te schakelen (zoals dimmen doe je met een lamp).
- `import time` — Dit laadt het time-gereedschap zodat we kunnen zeggen: "wacht even" (met `time.sleep`)

### Stap 1: Buzzer voorbereiding
```python
BZ = PWM(Pin(22))
```
**Wat gebeurt hier?**
- We maken verbinding met Pin 22 (dit is waar de buzzer op aangesloten is)
- `PWM` maakt er een "geluidsmachine" van — iets wat we kunnen aan en uit zetten

### Stap 2: Standaard geluidshoogte instellen
```python
BZ.freq(1000)
```
**Wat gebeurt hier?**
- `freq(1000)` betekent: de frequentie (pitch/hoogte) is 1000 Hz
- Dit is ongeveer een middelste toon — niet heel hoog, niet heel laag
- (Hogere getallen = hogere toon, lagere getallen = lagere toon)

### Stap 3: Muzieknoten definiëren
```python
CM = [0, 330, 350, 393, 441, 495, 556, 624]
```
**Wat gebeurt hier?**
- Dit is een lijst met verschillende frequenties (tonen)
- `CM[0] = 0` — geen geluid (stil)
- `CM[1] = 330 Hz` — lage Do note
- `CM[2] = 350 Hz` — Re note
- `CM[3] = 393 Hz` — Mi note
- ... en zo verder
- Deze list is zoals een piano keyboard — elk getal is een ander toetje!

### Stap 4: De melodie kiezen
```python
song = [CM[1],CM[1],CM[5],CM[5],CM[6],CM[6],CM[5],CM[4],CM[4],CM[3],CM[3],CM[2],CM[2],CM[1],]
```
**Wat gebeurt hier?**
- Dit is de volgorde van noten die we willen afspelen
- `CM[1]` twee keer = "Do Do"
- `CM[5]` twee keer = "Sol Sol"
- We spelen deze noten na elkaar af — dit vormt een melodie!

### Stap 5: Ritme instellen
```python
beat = [ 0.5,0.5,0.5,0.5,0.5,0.5,1,0.5,0.5,0.5,0.5,0.5,0.5,1,]
```
**Wat gebeurt hier?**
- Dit bepaalt HOE LANG elke noot speelt (in seconden)
- `0.5` = halve seconde speelt deze noot
- `1` = hele seconde speelt deze noot
- Zo krijgt elke noot zijn eigen duur!

### Stap 6: De muziekfunctie
```python
def music():
        print('Speelt liedje ...')
        for i in range(len(song)):
            BZ.duty_u16(500)      # Zet buzzer aan (500 betekent: 50% kracht)
            BZ.freq(song[i])       # Speel noot nummer i
            time.sleep(beat[i])    # Wacht zo lang als de beat aangeeft
            BZ.duty_u16(0)         # Zet buzzer uit (pauze)
            time.sleep(0.01)       # Kleine pauze van 0.01 seconde tussen noten
```
**Wat gebeurt hier?**
- Dit is ons "recept" om muziek af te spelen
- We gaan door alle noten (de loop `for i in range(len(song))`)
- Voor elke noot:
  - Zet buzzer aan
  - Stel frequentie in (welke noot speelt)
  - Wacht zo lang als de beat aangeeft
  - Zet buzzer uit (pauze)
  - Wacht heel kort

### Stap 7: Muziek afspelen
```python
music()
print("Einde")
```
**Wat gebeurt hier?**
- `music()` — We voeren onze muziekfunctie uit = het lied begint!
- `print("Einde")` — Na afloop print het "Einde"

---

## Samengevat
1. **Voorbereiding** — We maken verbinding met pin 22 waar de buzzer zit
2. **Tonen definiëren** — We zeggen wat de frequenties zijn (Do, Re, Mi...)
3. **Volgorde bepalen** — We zeggen welke noten we willen spelen
4. **Ritme toevoegen** — We zeggen hoe lang elke noot moet spelen
5. **Afspelen** — We voeren de musik() functie uit

De robot laat de buzzer verschillende tonen afspelen volgens de opgegeven frequenties en duur — zo kun je muziek maken met de buzzer!
