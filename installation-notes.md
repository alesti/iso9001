# Installationsnotizen ISO9001

For english readers: Please read the [README](README.md), sorry.

Aleks' Ergänzungen zur [Original Doku Hector9000](https://cdn.hackaday.io/files/1615856913252640/H9000_ger_V0.2a.pdf) zum Cocktailbot [Hector9000](https://hackaday.io/project/161585-hector-9000).

[Bilder vom Bau und Konzeptionskram](https://photos.app.goo.gl/biA2kgEKCT5nZmoh6) 

## Installation suffkopp (raspi)

[Raspbian Buster Lite](https://www.raspberrypi.org/downloads/raspbian/)
mit Etcher. 

* raspi-config: SSH angeklemmt, Wifi, Lokalisierung, alle Schnittstellen erstmal an.
* Accounts angelegt (aleks, sudo), cocktail für den ganzen Scheiss. pi => /bin/false,  pi pw gescrambled, auto security updates.
* cocktail in die wesentlichen Gruppen gestopft
* sshd publickey-auth only
* Zusätzliche Packages: 

```
etckeeper git vim screen python3-dev python3-pip python3-smbus 
i2c-tools python3-rpi.gpio adafruit-circuitpython-servokit
xinit lxde-core lxterminal lxappearance lightdm unclutter
```

### LXDE und Kioskmode 

Die Anwendung läuft im Fullscreen auf dem HDMI-Display. Ich will, dass
diese alleine hochkommt, also alleine in X gebootet und die Anwendung
gestartet wird.

In `raspi-config, boot options` Desktop, autologin einschalten,
Login-User in `/etc/lightdm/lightdm.conf` den autologin User setzen.

In `/etc/xdg/lxsession/LXDE/autostart` eintragen:

```
# https://www.danpurdy.co.uk/web-development/raspberry-pi-kiosk-screen-tutorial/

@lxpanel --profile LXDE
@pcmanfm --desktop --profile LXDE
@xset s off
@xset -dpms
@xset s noblank
```

In `/home/cocktail/bin/` ein Startscript anlegen - die Anwendung hat
lokale Pfade, ein `python3 path/to/repo/src/main.py` tut nicht in
autostart. Dann nochmal in `/home/cocktail/.config/lxsession/LXDE/autostart` wie oben, plus `@/home/cocktail/bin/autostart.sh` - in der Systemautostart tut das nicht - hab gerade nicht genug Energie, um da reinzukriechen.
Anscheinend bei jedem zweiten X Neustart? So ein Scheiss.


Zum Kiokmode: [Raspi Kiosk
Mode](https://www.danpurdy.co.uk/web-development/raspberry-pi-kiosk-screen-tutorial/), [Tipps](https://github.com/MobilityLab/TransitScreen/wiki/Raspberry-Pi).

## Display

Nach Doku die `/boot/config.txt` ändern:

```
# Waveshare 7inch HDMI LCD (C) Display
# https://www.waveshare.com/w/upload/c/cc/7inch_HDMI_LCD_%28C%29_User_Manual.pdf
max_usb_current=1
hdmi_group=2
hdmi_mode=87
hdmi_cvt 1024 600 60 6 0 0 0
hdmi_drive=1
# display_rotate=1 #1: 90; 2: 180; 3: 270
``` 

Booten, fertig.

[Original Wiki](https://www.waveshare.com/wiki/7inch_HDMI_LCD_(C)),
## ATX Netzteil 

Ist genormt, siehe [PSU as workbench supply](https://www.electronics-tutorials.ws/blog/convert-atx-psu-to-bench-supply.html):

Farbe | Spannung | Info
----- | ---- | ----
orange | 3,3V |
rot|  5V | 
gelb| 12V|
grün| 5V switch on| auf Masse ziehen
schwarz|  Masse|

Um das Netzteil ohne Motherboard zu benutzen, PIN16/grün auf Masse ziehen. Das Netzteil braucht eine (sehr geringe) Grundlast, damit es läuft.

Masse: Tiefe 140mm plus Kabelbaum, 80mm hoch, 150mm breit. M3 Gewinde zum Anschrauben.

## Adafruit PCA9685 Servo Driver

[Wie Servodriver anschliessen?](https://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi/configuring-your-pi-for-i2c)

Testen, ob er da ist:

```
root@suffkopp:~# sudo i2cdetect -y 1
```
[Adafruit Servo Driver](https://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi/hooking-it-up), [Bild in gross](https://cdn-learn.adafruit.com/assets/assets/000/069/564/original/components_raspi_pca9685_i2c_with_servo.jpg?1547757668)

vs. Laut Doku: Erstmal RASPI BCM2 (Pin 3) => PCA9685 SDA; RASPI BCM 3 (Pin 5) => PCA9685 SCL.
5V vom Netzteil.

## Relais für Pumpe und Zeug

Relaisboard besser [mit Treiber](http://www.susa.net/wordpress/2012/06/raspberry-pi-relay-using-gpio/) fahren, mindestens nen 1Kohm Widerstand pro GPIO.

Weiteres Relais für Beleuchtung, eventuell Spiegelkugel oder anderer Aufmerksamkeitsschnickschnack.

## Stepper Motor

Ich verwende diesen [Motor](https://www.amazon.de/gp/product/B07GLMGQB3).

Farbe | PIN | Coil
----- | --- | ----
rot | A / 1 | 1
blau| C / 4 | 1
schwarz | B / 3 | 2 
grün | D / 6 | 2

## Waage

Schrauben in M5. 

Farbe | PIN 
----- | ---- 
Rot | E+ |
Schwarz | E-
Grün | A-
Weiss | A+
VCC | 3,3V

## Test von Servos, Relais, Stepper, Waage

Es gibt je ein (sehr primitives) Testscript, die die generelle Funktion des Relaisboards und des Servokontrollers testet, siehe unter hw-tests im Repo.

Die Servos drehen mit dem Testskript um XX° gegen den Uhrzeigersinn. 50° scheint ganz gut zu sein.

Zum Testen der Waage hab ich [HX711 Beispiele](https://github.com/gandalf15/HX711/blob/master/HX711_Python3/all_methods_example.py) genommen, einfach um rauszufinden, wie die Belegung der Drähte ist und welche Seite des Balkens unten ist.

Zum Testen des Steppers habe ich ein Skript nach https://www.rototron.info/raspberry-pi-stepper-motor-tutorial/ gebaut. Manchmal funktioniert es.
Es rappelt ziemlich (es sind nur [STEP und DIR (wie hier)](https://www.pololu.com/picture/view/0J3360) verbunden für den Test). 


## Software
### Kivy Installation

Als User cocktail - so wie es da steht.
Examples wohnen in `~/.local/share/kivy-examples/demo/showcase`

Das Touchdisplay funktioniert in Kivy nicht, auf dem LXDE Desktop aber. 
Geholfen hat eine Ergänzung in `.kivy/config.ini` ([Touch Input not recogonised in Kivy](https://groups.google.com/forum/#!msg/kivy-users/7a8yz1oZ3Z0/Asy14nx2BQAJ)):

```
mtdev_%(name)s = probesysfs,provider=mtdev
hid_%(name)s = probesysfs,provider=hidinput
```

### Hector Software Installation
`git clone https://github.com/H3c702/Hector9000.git`

`pip3 install --user -r requirements.txt`

## 3D Druck / Filament

Drucker: Prusa i3 MK3S, eingehaust

### Allgemein

Ich benutze hauptsächlich PETG, geht wunderbar, am liebsten das von Prusa.
Das Projekt ist zu 90% mit PETG von 3djake gedruckt, das war aber ziemlich scheisse aufgespult, mir ist ein paar Mal die Rolle abgesprungen, kaufe ich nicht noch mal.

### Gleitlager, Ventilzungen

Für das Gleitlager und die Ventilzungen benutze ich wie im Original vorgeschlagen Igus Iglidur 150-PF ([Datenblatt](doc-extern/iglidur-I-150-PF-Verarbeitungshinweise-FDM.pdf)). 

* Bett-Temperatur 60°
* Düsentemperatur erste Schicht 250°, alle anderen 245°
* Bauteillüfter aus
* Einstellung in PrusaSlicer Filamenttype PLA (keine Ahnung, was das für Auswirkungen hat)
* Klebestift auf dem Druckbett. Ich hasse das, aber ohne gehts leider nicht

## Hardware Montage
### Ventile

Es sind vorsichtige Nacharbeiten notwendig, anscheinend insbesondere an den Schlitzen, in die die Ventilzungen eingesetzt werden.

1. Die Servos müssen als erstes in die Halterung
3. Ventilzungen
2. Schlauch
4. Servokopf

Punkt 1 und 2 kann man tauschen, aber das Servo bekommt man nicht mehr in die Halterung, wenn die Zungen bereits montiert sind.

Eine Abdeckung aus Plexiglas wie beim Orginal Hector9000 wäre schon schön, ~~anscheinend schneidet [kunstoffplattenonline](kunststoffplattenonline.de) auch unter 10cm zu~~ - nein, tun sie nicht, wenn man was in den Warenkorb legt, muss es mindestens 10cm haben.

### Display

Anderes HDMI-Kabel mit abgewinkeltem oder kurzem Stecker nötig, nicht
viel Platz im Gehäuse -- selbst mit abgewinkeltem Stecker ist das kacka, weil das dann mit dem Micro-USB kollidiert.
Wahrscheinlich haben die das im Original mit einem Flachbandkabel realisiert und den eigenen Stecker erst an der Rückwand des Rahmens eine HDMI-Buchse angeschlossen.

Ich hab das jetzt ausgebrochen und gut ist.

### Notaustaster (Pumpe)

Sinnvoll? Verhindert eventuell Sauereien.

### Beleuchtung

Eventuell was mit einem großen Pi-Hat, liegt hier rum. Oder was mit DMX, Minispiegelkugel und Farbwechsler. 

## Mindestabmessungen Montage in mm

### [Ventilgehäuse](https://photos.google.com/share/AF1QipNlWgx3b4bBSz2jLp8mGbXrvzWVxSNpFHqbeOVvxxnjIGTGQ0EjMjqpo94DNAowvg/photo/AF1QipPRc8o6I_D1Nod3YFpAS-qCG68FnTidyAR73DMF?key=MGdOcG9Cd2RHd2R5Q2p6MzljdEdwZjMtbndiVHJB):

* Platz für Servoausschnitt: 15 - 20 (Servo) - 15 (macht zusammen 50)
* Platz für Servoausschnitt: 16 - 58 (Servo) - 16 (macht zusamnen 90)

[Alle Ventilgehäuse zusammen](https://photos.google.com/share/AF1QipNlWgx3b4bBSz2jLp8mGbXrvzWVxSNpFHqbeOVvxxnjIGTGQ0EjMjqpo94DNAowvg/photo/AF1QipMRqTnI6m-zkJFATKUl3cBvPN3G64qVepazVG0M?key=MGdOcG9Cd2RHd2R5Q2p6MzljdEdwZjMtbndiVHJB)

* 6 Stück nebeneinander 300, immer noch 90 hoch :)
* Abstand zwischen den Reihen im Testbrett 47. Vielleicht später 50. Weniger eher nicht, sonst knicken die Schläuche zu stark.

### Arm 
#### Höhe Unterkante Arm über dem Boden

* Waage 16 (plus 2mm Spalt)
* Glas ([Ikea Pokal, 35cl](https://www.ikea.com/de/de/p/pokal-glas-klarglas-10270478/)) 140, (oder Glas ([Ikea, Vardagen, 43cl](https://www.ikea.com/de/de/p/vardagen-glas-klarglas-70313106/)) 130, kleiner, mehr Fassungsvermögen)
* etwas Platz zum Arm: 15

=>  180 sollten es sein.

=> __Testaufbau__ hat 220! Das ist zuviel!

#### Abstand zwischen Oberkante Arm und unterem Ventilkörper

=> 55 

* Arm: 15,5 
* Abstand zum Abtropfarm ~2 

#### Länge Arm, Position Zahnstange

* Erstmal grob 270, das ist auf jeden Fall zu lang, kann wohl um 80 gekürzt werden (ist rot markiert).
* Position ausgefahren: Freie Länge von Wand bis Armende (ohne Schlauchhalter) 120.

### Glockenkram / Finger

Der `Mittelpunkt der Glocke` soll 100mm vom Drehpunkt des Fingers entfernt sein. 
~~Ich nehme mal an, dass der Drehpunkt auch auf der gleichen Höhe sein muss wie der Glockenknopf.~~ [Nee, ausprobiert. Die untere Servobefestigung muss auf der gleichen Höhe sein wie der Tisch](https://photos.google.com/share/AF1QipNlWgx3b4bBSz2jLp8mGbXrvzWVxSNpFHqbeOVvxxnjIGTGQ0EjMjqpo94DNAowvg/photo/AF1QipNqxUpgVL77Z1uqbnDNZ0QqbEzxEzWZy4f_9zic?key=MGdOcG9Cd2RHd2R5Q2p6MzljdEdwZjMtbndiVHJB).

* Höhe Glocke mit gedrucktem Unterbau: 61 (jetzt eher irrelevant)
* Höhe Servogehäuse 78
* Abstand Servogehäuse unten (Kabelseite) bis Drehpunkt: 30
* Abstand vom Fingerloch (Unterkante) bis Servogehäuse Oberkante): 40
* Abstand vom Fingerloch (Oberkante) bis Servogehäuse Oberkante): 62


## Gehäuse

Das ganze als Flightcase bauen, bei dem man die Vorder- und Rückseite
als Deckel abnehmen kann (`double door rack`). Mir gefällt ohne Verhandlungen bisher [Casebuilder](https://www.casebuilder.com/de/benutzerdefinierte-flightcase-html/rackcasedouble/entwurf) am besten.

Es ist unklar, wie weit die Griffmulden in den Bauraum reinreichen. Mail ist raus. Eventuell müssen die Griffe in die Deckel, damit das nicht stört.

Um die passenden Schrauben zu bestellen zu können, geh ich erstmal von einer 9mm Siebdruckplatte als Rückwand, Servohalterung und so weiter aus.

Es gibt 0,8mm Alublech bei Bauhaus (bis 1000 x 2000mm), das lässt sich gut mit normalen Werkzeugen bearbeiten.
Oder bei [Feld
Schlosserbedarf](https://www.feld-eitorf.de/laserzuschnitt/rechteck-mit-individuellen-ausschnitten)
komplett konfigurieren - dann ist Edelstahl geiler...

Die Siebdruckplatte dann mit Alublech beplanken (Kleben, Popnieten), ebenso für den Tisch verfahren und auch die Seitenwände und den Flaschenboden damit auskleiden (wegen der geilen Reflexionen).

Blech für Tisch vorne abkanten und 2cm überstehen lassen als Blendschutz für die LED-Beleuchtung. Oder einfach mit einem Alu-L-Profil, wahrscheinlich einfacher.

### Maße (erste Näherung)

#### Mechanik, Oberteil

* Allein für die Mechanik reicht eine Höhe des oberen Teils von 520mm, mit besseren Abständen 570:

| was | Höhe | Höhe von oben addiert bis Unterkante Item | 
|-----|------|-----------------------|
| Platz über erster Ventilreihe| 50 |  50 |
| 1. Ventilreihe | 90 | 140 |
| Platz zwischen Ventilreihen | 50 | 190 |
| 2. Ventilreihe | 90 | 280 |
| Platz zwischen Ventilreihe und Arm | 55 | 335 |
| Arm bis Unterkante Tropfenfänger | 55 | 390 |
| Unterkante Tropfenfänger bis Tisch | 180 | **570**
	
und eine Breite von 420mm auf dem Testbrett. Mit allem sollten 600mm Breite locker reichen.

Also **600 x 570** für das Mechanikbrett. Ich hab mit [Fusion360](mechanikplatte.f3d) das ganze Brett durchkonstruiert. Die Idee ist es, die entstandene 1:1 [Zeichnung](mechanikplatte-bemasst-a0.pdf) auszudrucken, auf die Platte zu kleben und dann auszudremeln.

Enventuell ist es aber auch gar nicht so teuer, das cnc-fräsen zu
lassen.

#### Tiefe von alles 

* Tiefe Tisch (auf dem Waage und Glocke stehen) 220mm.
* Tiefe Rückseite (ohne Technikträgerbrett, 9mm plus Alublech) mindestens 150mm (das ist die Tiefe des Netzteils).
* Rückwand im unteren Bereich plus Netzteilhöhe 9mm plus Alublech
* Gesamttiefe also bisher 220 + 10 + 160 + 10 = 400

=> 500

#### Flaschenboden
* Literflaschen: Ø 90mm, Höhe 320mm plus Stopfen (20) pluss etwas Luft für den Schlauch 45mm, zusammen 385.
* 3x4 Flaschenfläche: 270 x 360
* Kanister 3 Liter: Fläche 150 x 115, Höhe 240
* Kanister 5 Liter: Fläche 190 x 145, Höhe 250

Auf eine Grundfläche von 600 x 420 bekommt man 3 5L Kanister und 12
Flaschen - mehr als genug.

#### Tisch

Für Waage und Glocke. 220 x 600.

#### Rückwand

Vom Boden bis 200 mm über Tischhöhe, dann kann das Netzteil dort montiert werden.

#### Gesamt

* Grundfläche 600 Breite x 420 Tiefe => 600 x 500
* Höhe Flaschenboden 400
* Höhe Tisch 10
* Höhe Oberteil 570

=> Casebuilder Standard, Birkensperrholz/PVC mit bunt

| Masse | Tiefe | Breite | Höhe |
|-------|-------|--------|------|
| innen | 500   | 600 | 980 |
| aussen |  |  |  | 

Und Art-Nr 0611 - F-Profil 9,1mm für den Waagentisch (beide Seiten, Rückseite an Mechanikwand), für Mechanikwand (beide Seiten), für Rückwand (beide Seiten, Boden).

Nachfragen:

* Tiefe der Griffe in den Seiten - sollten nicht in den Raum ragen, dann lieber Griffe, die aussen angeschraubt sind? Oder Griffe an die Deckel statt an die Seitenwände.
* Kantenschutz für Tischkante vorn und Oberkante Rückwand Art-Nr 0655 - U-Profil 9mm

