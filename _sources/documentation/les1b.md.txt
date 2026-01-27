# Les 1b: Interactief programmeren met Python

Welkom bij het vervolg van les 1a! In de vorige les heb je geleerd hoe je tekst kunt printen, variabelen kunt maken en eenvoudige berekeningen kunt doen. Nu gaan we je programma's interactief maken, zodat ze kunnen reageren op wat de gebruiker invoert en beslissingen kunnen nemen.

## Leerdoelen

Aan het einde van deze les kun je:
- Input van de gebruiker vragen en gebruiken
- Keuzes maken met if-statements
- Code herhalen met loops (for en while)
- Een interactief programma maken dat reageert op gebruikersinvoer

## Input: Vragen aan de gebruiker

Tot nu toe hebben we alleen maar dingen geprint naar het scherm. Maar wat als je programma informatie van de gebruiker wil krijgen? Daarvoor gebruik je `input()`.

### Basis voorbeeld:
```python
naam = input("Wat is je naam? ")
print("Hallo " + naam + "!")
```

**Wat gebeurt er?**
1. Het programma stopt en wacht op input van de gebruiker
2. De gebruiker typt iets in en drukt op Enter
3. Wat de gebruiker heeft ingetypt wordt opgeslagen in de variabele `naam`
4. Het programma print een begroeting met de naam

### Let op: Input is altijd tekst!
Wanneer je `input()` gebruikt, krijg je altijd een **string** (tekst) terug, zelfs als de gebruiker een getal intypt.

```python
leeftijd = input("Hoe oud ben je? ")
print(type(leeftijd))  # Dit print: <class 'str'>
```

### Omzetten naar een getal

Als je met de invoer wilt rekenen, moet je het omzetten naar een getal:

```python
# Van tekst naar integer (geheel getal)
leeftijd_tekst = input("Hoe oud ben je? ")
leeftijd = int(leeftijd_tekst)
print("Volgend jaar ben je", leeftijd + 1)

# Of korter geschreven:
leeftijd = int(input("Hoe oud ben je? "))
print("Volgend jaar ben je", leeftijd + 1)
```

**Andere conversies:**
- `int()` - omzetten naar geheel getal
- `float()` - omzetten naar kommagetal
- `str()` - omzetten naar tekst

## Opdracht 1: Werken met input

**1.1** Vraag om de naam en leeftijd van de gebruiker:
```python
naam = input("Wat is je naam? ")
leeftijd = int(input("Hoe oud ben je? "))
print("Hallo " + naam + ", je bent " + str(leeftijd) + " jaar oud!")
```

**1.2** Maak een eenvoudige rekenmachine:
```python
getal1 = float(input("Geef het eerste getal: "))
getal2 = float(input("Geef het tweede getal: "))
som = getal1 + getal2
print("De som is:", som)
```

**1.3** Vraag om iemands favoriet eten en kleur:
```python
# Jouw code hier
# Vraag om favoriet eten en favoriet kleur
# Print een leuke zin met beide antwoorden
```

## If-statements: Keuzes maken

Met een **if-statement** kan je programma beslissingen nemen. Afhankelijk van een voorwaarde gebeurt er iets wel of niet.

### Basis structuur:
```python
leeftijd = int(input("Hoe oud ben je? "))

if leeftijd >= 18:
    print("Je bent volwassen!")
```

**Let op de structuur:**
- `if` gevolgd door een voorwaarde en een dubbele punt `:`
- De code die uitgevoerd moet worden staat **ingesprongen** (4 spaties of 1 tab)
- De inspringing is cruciaal in Python!

### If-Else: Twee mogelijkheden

```python
leeftijd = int(input("Hoe oud ben je? "))

if leeftijd >= 18:
    print("Je bent volwassen!")
else:
    print("Je bent nog minderjarig.")
```

### If-Elif-Else: Meerdere mogelijkheden

```python
cijfer = float(input("Wat is je cijfer? "))

if cijfer >= 8.0:
    print("Uitstekend!")
elif cijfer >= 7.0:
    print("Ruim voldoende!")
elif cijfer >= 5.5:
    print("Voldoende.")
else:
    print("Onvoldoende.")
```

**Hoe werkt dit?**
- Python controleert de voorwaarden van boven naar beneden
- Bij de eerste voorwaarde die waar is, wordt die code uitgevoerd
- De rest wordt overgeslagen
- `elif` is kort voor "else if"

### Vergelijkingsoperatoren

Je kunt verschillende dingen vergelijken:

| Operator | Betekenis | Voorbeeld |
|----------|-----------|-----------|
| `==` | Is gelijk aan | `x == 5` |
| `!=` | Is niet gelijk aan | `x != 5` |
| `>` | Groter dan | `x > 5` |
| `<` | Kleiner dan | `x < 5` |
| `>=` | Groter dan of gelijk aan | `x >= 5` |
| `<=` | Kleiner dan of gelijk aan | `x <= 5` |

**Let op:** Een enkel `=` is voor toewijzen, dubbel `==` is voor vergelijken!

```python
x = 5      # Toewijzen: x krijgt de waarde 5
x == 5     # Vergelijken: is x gelijk aan 5?
```

### Meerdere voorwaarden combineren

Je kunt voorwaarden combineren met `and` en `or`:

```python
leeftijd = int(input("Hoe oud ben je? "))
heeft_rijbewijs = input("Heb je een rijbewijs? (ja/nee) ")

if leeftijd >= 18 and heeft_rijbewijs == "ja":
    print("Je mag autorijden!")
else:
    print("Je mag nog niet autorijden.")
```

**Logische operators:**
- `and` - beide voorwaarden moeten waar zijn
- `or` - minstens één voorwaarde moet waar zijn
- `not` - keert de voorwaarde om

```python
# Voorbeelden
if leeftijd >= 18 and leeftijd < 65:
    print("Je bent in de werkende leeftijd")

if dag == "zaterdag" or dag == "zondag":
    print("Het is weekend!")

if not is_student:
    print("Je bent geen student")
```

## Opdracht 2: Werken met if-statements

**2.1** Controleer of een getal positief of negatief is:
```python
getal = int(input("Geef een getal: "))

if getal > 0:
    print("Het getal is positief")
elif getal < 0:
    print("Het getal is negatief")
else:
    print("Het getal is nul")
```

**2.2** Maak een wachtwoord checker:
```python
wachtwoord = input("Geef het wachtwoord: ")

# Controleer of het wachtwoord "python123" is
# Print "Toegang verleend!" of "Toegang geweigerd!"
```

**2.3** Controleer of iemand mag stemmen:
```python
leeftijd = int(input("Hoe oud ben je? "))
nationaliteit = input("Heb je de Nederlandse nationaliteit? (ja/nee) ")

# Iemand mag stemmen als ze 18 of ouder zijn EN de Nederlandse nationaliteit hebben
# Print of ze wel of niet mogen stemmen
```

**2.4** Maak een eenvoudig menu:
```python
print("=== MENU ===")
print("1. Koffie")
print("2. Thee")
print("3. Water")

keuze = input("Wat wil je drinken? (1/2/3) ")

# Gebruik if-elif-else om te printen wat ze hebben gekozen
```

## Loops: Code herhalen

Soms wil je een stuk code meerdere keren uitvoeren. Daarvoor gebruik je **loops** (lussen).

### For-loop: Vaste aantal herhalingen

Een **for-loop** gebruik je als je weet hoeveel keer iets herhaald moet worden.

```python
# Tel van 0 tot en met 4
for i in range(5):
    print(i)

# Uitvoer:
# 0
# 1
# 2
# 3
# 4
```

**Wat is `range()`?**
- `range(5)` geeft: 0, 1, 2, 3, 4 (5 getallen, begint bij 0)
- `range(1, 6)` geeft: 1, 2, 3, 4, 5 (van 1 tot 6, exclusief 6)
- `range(0, 10, 2)` geeft: 0, 2, 4, 6, 8 (stappen van 2)

### Voorbeelden van for-loops:

```python
# Tel van 1 tot en met 10
for i in range(1, 11):
    print(i)

# Print 5 keer "Hallo"
for i in range(5):
    print("Hallo")

# Tafel van 5
for i in range(1, 11):
    print("5 x", i, "=", 5 * i)
```

### Door een lijst heen loopen

Je kunt ook door een lijst met items loopen:

```python
kleuren = ["rood", "blauw", "groen", "geel"]

for kleur in kleuren:
    print("Mijn favoriete kleur is", kleur)
```

### While-loop: Herhalen tot een voorwaarde niet meer waar is

Een **while-loop** blijft draaien zolang een voorwaarde waar is.

```python
teller = 0

while teller < 5:
    print("Teller is:", teller)
    teller = teller + 1

print("Klaar!")
```

**Wat gebeurt er?**
1. Controleer of `teller < 5` waar is
2. Zo ja: voer de code uit en verhoog teller met 1
3. Ga terug naar stap 1
4. Zo nee: stop de loop

⚠️ **Let op voor oneindige loops!**
```python
# DIT STOPT NOOIT! (oneindige loop)
teller = 0
while teller < 5:
    print(teller)
    # Vergeten om teller te verhogen!
```

Zorg er altijd voor dat de voorwaarde op een gegeven moment niet meer waar is!

### When to use which?

- **For-loop**: Als je weet hoeveel keer iets herhaald moet worden
- **While-loop**: Als je wilt herhalen totdat een bepaalde voorwaarde niet meer waar is

```python
# For: Print 10 sterretjes
for i in range(10):
    print("*")

# While: Blijf vragen tot het antwoord correct is
antwoord = ""
while antwoord != "python":
    antwoord = input("Wat is de beste programmeertaal? ")
print("Correct!")
```

## Opdracht 3: Werken met loops

**3.1** Print de getallen 1 tot en met 20:
```python
# Jouw code hier met een for-loop
```

**3.2** Print alle even getallen van 0 tot en met 20:
```python
# Tip: gebruik range(0, 21, 2) of gebruik if om te checken of een getal even is
```

**3.3** Maak de tafel van 7:
```python
# Print: 7 x 1 = 7, 7 x 2 = 14, etc. tot 7 x 10 = 70
```

**3.4** Tel tot 100 met stappen van 10:
```python
# Print: 0, 10, 20, 30, ... 100
```

**3.5** Raadspel met while-loop:
```python
geheim_getal = 7
geraden = False

while not geraden:
    gok = int(input("Raad het getal (1-10): "))
    
    if gok == geheim_getal:
        print("Goed geraden!")
        geraden = True
    else:
        print("Helaas, probeer opnieuw!")
```

**3.6** Tel af van 10 naar 0:
```python
# Print: 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0
# Tip: gebruik range(10, -1, -1)
```

## Break en Continue

Soms wil je een loop eerder stoppen of een iteratie overslaan:

### Break: Stop de loop

```python
for i in range(10):
    if i == 5:
        break  # Stop de loop wanneer i 5 is
    print(i)

# Output: 0, 1, 2, 3, 4
```

### Continue: Sla deze iteratie over

```python
for i in range(10):
    if i == 5:
        continue  # Sla 5 over
    print(i)

# Output: 0, 1, 2, 3, 4, 6, 7, 8, 9
```

### Praktisch voorbeeld:

```python
# Zoek naar een specifiek woord
woorden = ["hond", "kat", "vogel", "vis"]

for woord in woorden:
    if woord == "vogel":
        print("Vogel gevonden!")
        break
    print("Zoeken...")
```

## Opdracht 4: Interactief programma maken

Nu gaan we alles combineren! Maak een interactief programma naar keuze:

### Optie A: Quiz programma
```python
print("=== QUIZ ===")
score = 0

# Vraag 1
antwoord = input("Wat is de hoofdstad van Nederland? ")
if antwoord.lower() == "amsterdam":
    print("Correct!")
    score = score + 1
else:
    print("Fout, het juiste antwoord is Amsterdam")

# Vraag 2
antwoord = input("Hoeveel poten heeft een spin? ")
if antwoord == "8":
    print("Correct!")
    score = score + 1
else:
    print("Fout, het juiste antwoord is 8")

# Vraag 3 - voeg zelf een vraag toe!

print("Je score is:", score, "van de 3")
```

### Optie B: Rekenmachine menu
```python
print("=== REKENMACHINE ===")

while True:
    print("\n1. Optellen")
    print("2. Aftrekken")
    print("3. Vermenigvuldigen")
    print("4. Delen")
    print("5. Stop")
    
    keuze = input("Maak een keuze (1-5): ")
    
    if keuze == "5":
        print("Tot ziens!")
        break
    
    getal1 = float(input("Eerste getal: "))
    getal2 = float(input("Tweede getal: "))
    
    if keuze == "1":
        print("Resultaat:", getal1 + getal2)
    elif keuze == "2":
        print("Resultaat:", getal1 - getal2)
    elif keuze == "3":
        print("Resultaat:", getal1 * getal2)
    elif keuze == "4":
        if getal2 != 0:
            print("Resultaat:", getal1 / getal2)
        else:
            print("Fout: Kan niet delen door 0!")
    else:
        print("Ongeldige keuze!")
```

### Optie C: Raadspel met hints
```python
import random

geheim_getal = random.randint(1, 100)
pogingen = 0
max_pogingen = 10

print("=== RAADSPEL ===")
print("Ik denk aan een getal tussen 1 en 100")
print("Je hebt", max_pogingen, "pogingen")

while pogingen < max_pogingen:
    gok = int(input("\nJouw gok: "))
    pogingen = pogingen + 1
    
    if gok == geheim_getal:
        print("🎉 Gefeliciteerd! Je hebt het geraden in", pogingen, "pogingen!")
        break
    elif gok < geheim_getal:
        print("Te laag! Je hebt nog", max_pogingen - pogingen, "pogingen over")
    else:
        print("Te hoog! Je hebt nog", max_pogingen - pogingen, "pogingen over")
else:
    print("\nHelaas, je pogingen zijn op! Het getal was:", geheim_getal)
```

**Opdracht:** Kies een van de drie programma's hierboven, typ het over en test het. Probeer het daarna uit te breiden met:
- Meer vragen/opties
- Betere foutafhandeling
- Extra functies

## Veelgemaakte fouten en oplossingen

### Fout 1: Vergeten om input om te zetten
```python
# ❌ Fout
leeftijd = input("Hoe oud ben je? ")
print(leeftijd + 1)  # ERROR!

# ✅ Correct
leeftijd = int(input("Hoe oud ben je? "))
print(leeftijd + 1)
```

### Fout 2: Verkeerde inspringing
```python
# ❌ Fout
if leeftijd >= 18:
print("Volwassen")  # ERROR: moet ingesprongen zijn

# ✅ Correct
if leeftijd >= 18:
    print("Volwassen")
```

### Fout 3: = in plaats van ==
```python
# ❌ Fout
if x = 5:  # ERROR: dit is toewijzen, niet vergelijken
    print("x is 5")

# ✅ Correct
if x == 5:
    print("x is 5")
```

### Fout 4: Oneindige loop
```python
# ❌ Fout
teller = 0
while teller < 10:
    print(teller)
    # Vergeten om teller te verhogen!

# ✅ Correct
teller = 0
while teller < 10:
    print(teller)
    teller = teller + 1
```

## Tips en tricks

💡 **Tip 1:** Gebruik duidelijke variabelennamen
```python
# Niet zo goed
x = input("Naam: ")

# Beter
naam = input("Naam: ")
```

💡 **Tip 2:** Test je code stap voor stap
- Schrijf niet alle code in één keer
- Test elke functie apart
- Voeg dan pas de volgende functie toe

💡 **Tip 3:** Gebruik comments om je code uit te leggen
```python
# Vraag om de leeftijd van de gebruiker
leeftijd = int(input("Hoe oud ben je? "))

# Controleer of de gebruiker volwassen is
if leeftijd >= 18:
    print("Je bent volwassen!")
```

💡 **Tip 4:** Let op datatypes bij vergelijkingen
```python
# Dit werkt niet zoals je verwacht!
leeftijd = input("Hoe oud ben je? ")  # Dit is een string!
if leeftijd >= 18:  # Vergelijkt strings, niet getallen!
    print("Volwassen")

# Beter:
leeftijd = int(input("Hoe oud ben je? "))
if leeftijd >= 18:
    print("Volwassen")
```

## Samenvatting

In deze les heb je geleerd:
- ✅ Input vragen met `input()` en omzetten met `int()` en `float()`
- ✅ Keuzes maken met if, elif en else
- ✅ Vergelijkingsoperatoren gebruiken: `==`, `!=`, `>`, `<`, `>=`, `<=`
- ✅ Logische operators gebruiken: `and`, `or`, `not`
- ✅ Code herhalen met for-loops en while-loops
- ✅ `range()` gebruiken voor for-loops
- ✅ Loops stoppen met `break` en overslaan met `continue`
- ✅ Interactieve programma's maken

## Extra oefeningen (voor thuis)

**Opdracht A:** BMI Calculator
```python
# Vraag om lengte (in meters) en gewicht (in kg)
# Bereken de BMI: gewicht / (lengte * lengte)
# Print of de persoon ondergewicht, normaal gewicht of overgewicht heeft
# BMI < 18.5: ondergewicht
# BMI 18.5-25: normaal
# BMI > 25: overgewicht
```

**Opdracht B:** Countdown timer
```python
# Vraag om een getal
# Tel af van dat getal naar 0
# Print elke seconde een getal lager
# Bij 0: print "Tijd is om!"
```

**Opdracht C:** Wachtwoord generator
```python
# Vraag hoeveel letters het wachtwoord moet hebben
# Genereer een wachtwoord met letters en cijfers
# Tip: gebruik de random module
```

**Opdracht D:** Gemiddelde berekenen
```python
# Vraag hoeveel cijfers de gebruiker wil invoeren
# Gebruik een loop om alle cijfers op te vragen
# Bereken en print het gemiddelde
```

**Opdracht E:** FizzBuzz
```python
# Print de getallen 1 tot en met 100
# Maar: als het getal deelbaar is door 3, print "Fizz"
# Als het deelbaar is door 5, print "Buzz"
# Als het deelbaar is door beide, print "FizzBuzz"
# Tip: gebruik de modulo operator %
```


