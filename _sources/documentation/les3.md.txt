# Les 3: Programmeren van sensoren

Op de pico-robot zijn verschillende sensoren aanwezig die gebruikt kunnen worden om de omgeving te detecteren. In deze les leer je hoe je deze sensoren kunt programmeren en gebruiken in je robotprojecten.

## Lichtsensoren
Er zijn twee lichtsensoren op de pico-robot.

::::{grid} 2
:::{grid-item-card} 
![Image](../images/lightsensor1.jpg)
:::
:::{grid-item-card}
![Image](../images/lightsensor2.jpg)
:::
::::

Deze sensoren kunnen de hoeveelheid licht in de omgeving meten. Dit doen ze met behulp van een fotoweerstand die de weerstand verandert afhankelijk van de hoeveelheid licht die erop valt. De gemeten waarden kunnen worden gebruikt om beslissingen te nemen in je robotprogramma, zoals het volgen van een lichtbron of het vermijden van donkere gebieden. De waarden die de lichtsensoren teruggeven liggen tussen 0 (geen licht) en 65535 (veel licht). De waarde van de lichtsensoren kan worden uitgelezen met behulp van de ADC (Analog to Digital Converter) functionaliteit van de microcontroller.

Een ADC is een apparaat dat een analoog signaal (zoals de spanning van een sensor) omzet in een digitaal signaal dat door de microcontroller kan worden verwerkt. In dit geval wordt de analoge spanning van de lichtsensoren omgezet in een digitale waarde tussen 0 en 65535.

Hier is een voorbeeldcode om de lichtsensoren uit te lezen en de waarden op de console weer te geven:

```python
from pico_car import ds, SSD1306_I2C
from machine import Pin, I2C, ADC
import time

# Light1 -> GP27
# Light2 -> GP26
light1 = machine.ADC(27)
light2 = machine.ADC(26)

while True:
    # Lees waarden uit
    LightS1 = light1.read_u16()
    LightS2 = light2.read_u16()
    print("light1 is %d"%(LightS1) )
    print("light2 is %d"%(LightS2) )
    time.sleep(0.5)
```
### Opdracht
Copieer de bovestaande code in een eigen bestand (gemaakt in Thonny) en voer deze uit op de pico-robot. Observeer de waarden die worden weergegeven op de console terwijl je de lichtsensoren blootstelt aan verschillende lichtomstandigheden (gebruik de zaklamp van je telefoon als lichtbron om op de sensor te schijnen).
    
## Ultrasonische sensor
Een ultrasonische sensor meet de afstand tot een object door geluidsgolven uit te zenden en de tijd te meten die het duurt voordat het geluid terugkeert na het weerkaatsen op het object. Dit maakt het mogelijk om obstakels te detecteren en afstanden te meten, wat handig is voor navigatie en botsingsvermijding. Op de pico-robot is een ultrasonische sensor gemonteerd die kan worden gebruikt om afstanden te meten.
![image](../images/ultrasoonsensor.jpg)

De ultrasonische sensor werkt door het uizenden van een onhoorbaar ultrasonisch signaal via een zender (transducer). Wanneer dit signaal een object raakt, wordt het teruggekaatst en opgevangen door een ontvanger (receiver). De tijd die het signaal nodig heeft om heen en terug te reizen wordt gemeten, en op basis daarvan kan de afstand tot het object worden berekend.
![inmage](../images/ultrasonic-sensor-working2.gif)
***Bron: [Ultrasonic sensor HC-SR04 with Arduino](https://arnin.in/sensors/ultrasonic-sensor-hc-sr04-with-arduino/?srsltid=AfmBOor5WMsG7SSVyTevzlf4CACYMkjzvcJpYzCU9Wl_XgBbt-MC2_tu)***

```python
import time
from machine import Pin, I2C
from pico_car import SSD1306_I2C, ultrasonic
# Initialiseer ultrasone sensor
ultrasonic = ultrasonic()

while True:
    # Lees afstand uit
    distance = ultrasonic.Distance_accurate()
    print("distance is %d cm"%(distance) )
    time.sleep(1)
```

### Opdracht
Copieer de bovestaande code in een eigen bestand (gemaakt in Thonny) en voer deze uit op de pico-robot. Observeer de waarden die worden weergegeven op de console terwijl je voor de sensor een voorwerp(je hand kan ook) houd op verschillende afstanden van de sensor.

## Trackingsensoren
![image](../images/trackingsensors.jpg)