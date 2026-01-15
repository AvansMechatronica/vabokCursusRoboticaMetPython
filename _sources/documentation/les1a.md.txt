# Les 1a: Introductie in Python programmeren

Welkom bij de eerste les! In deze les ga je kennismaken met programmeren. We gaan werken met Python, een programmeertaal die veel wordt gebruikt en relatief makkelijk te leren is. Aan het einde van deze les kun je:
- Uitleggen wat een programmeertaal is
- Eenvoudige Python programma's schrijven
- Code uitvoeren in een online ontwikkelomgeving
- Werken met variabelen en basisbewerkingen

## Wat is een programmeertaal?

Een **programmeertaal** is een taal waarmee je instructies aan een computer kunt geven. Net zoals je met Nederlands instructies aan een persoon geeft ("Pak een kop koffie"), gebruik je een programmeertaal om de computer te vertellen wat hij moet doen.

Computers begrijpen geen Nederlands of Engels. Ze werken met hele precieze instructies in een taal die ze kunnen interpreteren. Python is zo'n taal - een soort tussenpersoon tussen jouw ideeën en wat de computer begrijpt.

**Voorbeeld uit het dagelijks leven:**
- Je wilt een lamp aanzetten → Je drukt op de schakelaar
- Je wilt dat een robot vooruit rijdt → Je schrijft code die zegt: "rijd vooruit"

## Wat is Python?

**Python** is een populaire programmeertaal die veel wordt gebruikt voor verschillende toepassingen:
- **Websites** maken (zoals Instagram en Spotify)
- **Data analyseren** (bijvoorbeeld verkoopcijfers verwerken)
- **Robots aansturen** (zoals we in deze cursus gaan doen!)
- **Apps** ontwikkelen
- **Kunstmatige intelligentie** (zoals ChatGPT)

### Waarom Python?
Python is ideaal om te leren programmeren omdat:
1. De code lijkt op gewone Engelse zinnen en is goed leesbaar
2. Er is veel hulp en uitleg online te vinden
3. Je kunt er snel resultaten mee boeken
4. Het wordt veel gebruikt in het bedrijfsleven

## Je eerste stappen: Een online ontwikkelomgeving gebruiken

Om te kunnen programmeren heb je een plek nodig waar je code kunt schrijven en uitvoeren. Dit noemen we een **IDE** (Integrated Development Environment), oftewel een ontwikkelomgeving.

In deze les gebruiken we [online-python.com](https://www.online-python.com/). Dit is een website waar je direct kunt beginnen met programmeren, zonder dat je iets hoeft te installeren op je computer.

### Stap voor stap aan de slag:

**Stap 1:** Open je webbrowser (Chrome, Firefox, Edge, etc.)

**Stap 2:** Ga naar [https://www.online-python.com/](https://www.online-python.com/)

**Stap 3:** Je ziet nu een scherm met:
- Links: een **code-editor** (hier typ je je code)
- Rechts of onder: een **uitvoervenster** (hier zie je het resultaat)

**Stap 4:** Typ het volgende in de editor:
```python
print("Hello, World!")
```
> Let op: Verwijder eerst eventuele voorbeeldcode die al in de editor staat.

**Stap 5:** Klik op de groene knop "Run" (of druk op Ctrl+Enter)

**Stap 6:** Kijk naar het uitvoervenster. Je zou nu moeten zien:
```
Hello, World!
```

**Gefeliciteerd!** 🎉 Je hebt zojuist je eerste Python programma geschreven en uitgevoerd!

### Wat gebeurt er precies?

- `print()` is een **functie** in Python. Het zorgt ervoor dat tekst op het scherm verschijnt
- Tussen de haakjes `()` plaats je wat je wilt laten zien
- De aanhalingstekens `"..."` geven aan dat het om tekst gaat
- Het uitroepteken `!` aan het einde kun je weglaten, het is gewoon onderdeel van de tekst

## Opdracht 1: Experimenteer met print()

Probeer nu zelf de volgende opdrachten uit. Typ elke keer de code in de editor en klik op "Run":

**1.1** Print je eigen naam:
```python
print("Mijn naam is [jouw naam]")
```

**1.2** Print meerdere regels:
```python
print("Regel 1")
print("Regel 2")
print("Regel 3")
```

**1.3** Print getallen:
```python
print(42)
print(100)
```

**Vraag:** Zie je het verschil tussen `print("42")` en `print(42)`? Probeer beide!

## Variabelen: Informatie opslaan

Een **variabel** is als een doosje waar je informatie in kunt stoppen om later te gebruiken. Je geeft het doosje een naam, zodat je er gemakkelijk naar kunt verwijzen.

### Voorbeeld:
```python
naam = "Jan"
leeftijd = 18
print(naam)
print(leeftijd)
```

**Wat gebeurt hier?**
- We maken een variabele `naam` en stoppen daar de tekst "Jan" in
- We maken een variabele `leeftijd` en stoppen daar het getal 18 in
- We printen beide variabelen

### Regels voor variabelennamen:
✅ **Mag wel:**
- Kleine letters: `naam`, `leeftijd`
- Hoofdletters: `Naam`, `LEEFTIJD`
- Cijfers (maar niet aan het begin): `naam1`, `leeftijd2`
- Underscores: `mijn_naam`, `student_nummer`

❌ **Mag niet:**
- Beginnen met een cijfer: `1naam`
- Spaties: `mijn naam`
- Speciale tekens: `naam!`, `leeftijd@`

## Opdracht 2: Werken met variabelen

**2.1** Maak variabelen voor jezelf:
```python
mijn_naam = "..."  # Vul je eigen naam in
mijn_leeftijd = ...  # Vul je eigen leeftijd in
mijn_woonplaats = "..."  # Vul je woonplaats in

print(mijn_naam)
print(mijn_leeftijd)
print(mijn_woonplaats)
```

**2.2** Combineer tekst en variabelen:
```python
naam = "Lisa"
print("Hallo, ik ben " + naam)
```

**2.3** Maak een berekening:
```python
getal1 = 10
getal2 = 5
resultaat = getal1 + getal2
print(resultaat)
```

## Datatypes: Soorten gegevens

Python kent verschillende soorten gegevens. De belangrijkste zijn:

### 1. Tekst (String)
Tekst zet je tussen aanhalingstekens:
```python
naam = "Sarah"
stad = 'Amsterdam'  # Enkele of dubbele aanhalingstekens mogen beide
```

### 2. Gehele getallen (Integer)
Hele getallen zonder komma:
```python
leeftijd = 20
aantal_studenten = 25
```

### 3. Kommagetallen (Float)
Getallen met een decimaal (gebruik een punt, geen komma!):
```python
prijs = 19.99
temperatuur = 21.5
```

### 4. Waar/Onwaar (Boolean)
Kan alleen `True` of `False` zijn:
```python
is_student = True
heeft_rijbewijs = False
```

## Opdracht 3: Werken met verschillende datatypes

**3.1** Welk datatype is het?
```python
# Bepaal zelf wat voor soort gegevens dit zijn
a = "Python"           # Dit is een...?
b = 42                # Dit is een...?
c = 3.14              # Dit is een...?
d = True              # Dit is een...?
```

**3.2** Maak je eigen variabelen:
```python
# Maak een string variabele
favoriet_eten = "..."

# Maak een integer variabele
aantal_hobby = ...

# Maak een float variabele
gemiddeld_cijfer = ...

# Maak een boolean variabele
heeft_stage = ...
```

## Rekenen met Python

Python kan als een rekenmachine gebruikt worden!

### Basis rekenoperaties:
```python
# Optellen
print(5 + 3)        # Geeft: 8

# Aftrekken
print(10 - 4)       # Geeft: 6

# Vermenigvuldigen
print(6 * 7)        # Geeft: 42

# Delen
print(15 / 3)       # Geeft: 5.0

# Macht (tot de macht)
print(2 ** 3)       # Geeft: 8 (2 x 2 x 2)

# Gehele deling (zonder komma)
print(17 // 5)      # Geeft: 3

# Modulo (rest bij deling)
print(17 % 5)       # Geeft: 2
```

### Rekenen met variabelen:
```python
lengte = 10
breedte = 5
oppervlakte = lengte * breedte
print(oppervlakte)  # Geeft: 50
```

## Opdracht 4: Rekenopgaven

**4.1** Bereken de oppervlakte van een rechthoek:
```python
lengte = 12
breedte = 8
oppervlakte = ...  # Vul de berekening in
print("De oppervlakte is:", oppervlakte)
```

**4.2** Bereken je geboortejaar:
```python
huidig_jaar = 2024
leeftijd = ...  # Vul je leeftijd in
geboortejaar = ...  # Bereken je geboortejaar
print("Je bent geboren in ongeveer:", geboortejaar)
```

**4.3** Bereken het gemiddelde van drie cijfers:
```python
cijfer1 = 7.5
cijfer2 = 8.0
cijfer3 = 6.5
gemiddelde = ...  # Bereken het gemiddelde
print("Het gemiddelde is:", gemiddelde)
```

## Tips voor als het niet lukt

❌ **Foutmelding: SyntaxError**
- Controleer of je aanhalingstekens hebt gebruikt: `"tekst"`
- Controleer of de haakjes goed zijn: `print(...)`
- Let op hoofdletters: het is `print`, niet `Print`

❌ **Foutmelding: NameError**
- Je probeert een variabele te gebruiken die niet bestaat
- Controleer de spelling van je variabelennaam
- Heb je de variabele wel gemaakt voordat je hem gebruikt?

❌ **Er gebeurt niets**
- Heb je op "Run" geklikt?
- Staat er wel code in de editor?

❌ **Verkeerde uitvoer**
- Lees de code zorgvuldig na
- Controleer of je alles precies hebt overgetypt
- Controleer je berekeningen

## Samenvatting

In deze les heb je geleerd:
- ✅ Wat een programmeertaal is en waarom we Python gebruiken
- ✅ Hoe je een online Python omgeving gebruikt
- ✅ Je eerste code schrijven met `print()`
- ✅ Variabelen maken en gebruiken
- ✅ Verschillende datatypes: string, integer, float, boolean
- ✅ Rekenen met Python

## Extra oefeningen (voor thuis)

**Opdracht A:** Maak een programma dat informatie over jezelf print:
```python
# Jouw code hier
# Print je naam, leeftijd, opleiding en hobby
```

**Opdracht B:** Maak een simpele rekenmachine:
```python
getal1 = 25
getal2 = 8
# Print de uitkomst van: optellen, aftrekken, vermenigvuldigen en delen
```

**Opdracht C:** Bereken hoeveel seconden er in een week zitten:
```python
# Tip: 1 week = 7 dagen, 1 dag = 24 uur, etc.
```

