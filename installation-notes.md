# Installationsnotizen ISO9001

For english readers: Please read the [README](README.md), sorry.

Aleks' Ergänzungen zur [Original Doku Hector9000](https://cdn.hackaday.io/files/1615856913252640/H9000_ger_V0.2a.pdf) zum Cocktailbot [Hector9000](https://hackaday.io/project/161585-hector-9000)

## Installation suffkopp (raspi)

[Raspbian Buster Lite](https://www.raspberrypi.org/downloads/raspbian/)
mit Etcher. 

* raspi-config: SSH angeklemmt, Wlan, Lokalisierung, alle Schnittstellen erstmal an.
* Accounts angelegt (aleks, sudo), cocktail für den ganzen Scheiss. pi => /bin/false, sshd publickey-auth only, pi pw gescrambled, auto security updates.
* cocktail in die wesentlichen Gruppen gestopft
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
# @xscreensaver -no-splash

@xset s off
@xset -dpms
@xset s noblank
```

In `/home/cocktail/bin/` ein Startscript anlegen - die Anwendung hat
lokale Pfade, ein `python3 path/to/repo/src/main.py` tut nicht in
autostart. Dann nochmal in `/home/cocktail/.config/lxsession/LXDE/autostart` wie oben, plus `@/home/cocktail/bin/autostart.sh` - in der Systemautostart
tut das nicht - hab gerade nicht genug Energie, um da reinzukriechen.
Anscheinend bei jedem zweiten X Neustart? So ein Scheiss.

Das Touchdisplay funktioniert in Kivy nicht, auf dem LXDE Desktop aber. 
Geholfen hat eine Ergänzung in `.kivy/config.ini`

```
mtdev_%(name)s = probesysfs,provider=mtdev
hid_%(name)s = probesysfs,provider=hidinput
```

Links: [Raspi Kiosk
Mode](https://www.danpurdy.co.uk/web-development/raspberry-pi-kiosk-screen-tutorial/), [Tipps](https://github.com/MobilityLab/TransitScreen/wiki/Raspberry-Pi), [Touch Input not recogonised in Kivy](https://groups.google.com/forum/#!msg/kivy-users/7a8yz1oZ3Z0/Asy14nx2BQAJ).


## Adafruit PCA9685 Servo Driver

[Wie Servodriver anschliessen?](https://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi/configuring-your-pi-for-i2c)

Testen, ob er da ist:

```
root@suffkopp:~# sudo i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```
[Adafruit Servo Driver](https://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi/hooking-it-up), [Bild in gross](https://cdn-learn.adafruit.com/assets/assets/000/069/564/original/components_raspi_pca9685_i2c_with_servo.jpg?1547757668)

vs. Laut Doku: Erstmal RASPI BCM2 (Pin 3) => PCA9685 SDA; RASPI BCM 3 (Pin 5) => PCA9685 SCL.
5V vom Netzteil.

## Relais für Pumpe und Zeug

Relaisboard besser [mit Treiber](http://www.susa.net/wordpress/2012/06/raspberry-pi-relay-using-gpio/) fahren, mindestens nen 1Kohm Widerstand pro GPIO.


## ATX Netzteil 

Ist genormt, siehe [PSU as workbench supply](https://www.electronics-tutorials.ws/blog/convert-atx-psu-to-bench-supply.html):

Farbe | Spannung | Info
----- | ---- | ----
orange | 3,3V |
rot|  5V | 
gelb| 12V|
grün| 5V switch on| auf Masse ziehen
schwarz|  Masse|

Um das Netzteil ohne Motherboard zu benutzen, PIN16/grün auf Masse ziehen. Das Netzteil braucht eine (geringe) Grundlast, damit es läuft.

## Test von Servos und Relais

Es gibt je ein (sehr primitives) Testscript, die die generelle Funktion des Relaisboards und des Servokontrollers testet, siehe unter hw-tests im Repo.

Die Servos drehen mit dem Testskript um XX° gegen den Uhrzeigersinn. 50° scheint ganz gut zu sein.

## Stepper Motor

Noch ziemlich unklar, geht nach 
https://www.rototron.info/raspberry-pi-stepper-motor-tutorial/ gebaut
jedenfalls nicht.

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

```
[So Jul 28 09:02:39 2019] usb 1-1.1.3: New USB device found, idVendor=0eef, idProduct=0005, bcdDevice= 2.00
[So Jul 28 09:02:39 2019] usb 1-1.1.3: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[So Jul 28 09:02:39 2019] usb 1-1.1.3: Product: WS170120
[So Jul 28 09:02:39 2019] usb 1-1.1.3: Manufacturer: WaveShare
[So Jul 28 09:02:39 2019] usb 1-1.1.3: SerialNumber: ^Zë8157A920
[So Jul 28 09:02:39 2019] input: WaveShare WS170120 as /devices/platform/soc/3f980000.usb/usb1/1-1/1-1.1/1-1.1.3/1-1.1.3:1.0/0003:0EEF:0005.0001/input/input0
[So Jul 28 09:02:39 2019] hid-generic 0003:0EEF:0005.0001: input,hidraw0: USB HID v1.10 Device [WaveShare WS170120] on usb-3f980000.usb-1.1.3/input0
```

[Original Wiki](https://www.waveshare.com/wiki/7inch_HDMI_LCD_(C)),

### Kivy Installation

Als User cocktail - so wie es da steht.
Examples wohnen in `~/.local/share/kivy-examples/demo/showcase`

### Hector Installation
`git clone https://github.com/H3c702/Hector9000.git`

`pip3 install --user -r requirements.txt`

## 3D Druck / Filament

Drucker: Prusa i3 MK3S, eingehaust

### Allgemein

Ich benutze PETG, geht wunderbar. 
Am liebsten das von Prusa, das Projekt ist mit PETG von 3djake gedruckt.

### Gleitlager, Ventilzungen

Für das Gleitlager und die Ventilzungen benutze ich Igus Iglidur 150-PF ([Datenblatt](doc-extern/iglidur-I-150-PF-Verarbeitungshinweise-FDM.pdf)). 

* Bett-Temperatur 60°
* Düsentemperatur erste Schicht 250°, alle anderen 245°
* Bauteillüfter aus
* Einstellung in PrusaSlicer Filamenttype PLA (keine Ahnung, was das für Auswirkungen hat)
* Klebestift auf dem Druckbett. Ich hasse das, aber ohne gehts leider nicht

## Hardware Montage
### Ventile

Es sind vorsichtige Nacharbeiten notwendig, anscheinend insbesondere an den Schlitzen, in die die Ventilzungen eingesetzt werden.

1. Die Servos müssen als erstes in die Halterung
2. Schlauch
3. Ventilzungen
4. Servokopf

Punkt 1 und 2 kann man tauschen, aber das Servo bekommt man nicht mehr in die Halterung, wenn die Zungen bereits montiert sind.

Eine Abdeckung aus Plexiglas wie beim Orginal Hector9000 wäre schon schön.

### Display

Testweise mit den beiliegenden Kunststoffschrauben im Rahmen montiert.
Anderes HDMI-Kabel mit abgewinkeltem oder kurzem Stecker nötig, nicht
viel Platz im Gehäuse.

### Beleuchtung

Eventuell was mit einem großen Pi-Hut, liegt hier rum. Oder was mit DMX,
Minispiegelkugel und Farbwechsler

### Gehäuse

Das ganze als Flightcase bauen, bei dem man die Vorder- und Rückseite
als Deckel abnehmen kann. 

Um die passenden Schrauben zu bestellen zu können, geh ich erstmal von einer 12mm Siebdruckplatte als Rückwand, Servohalterung und so weiter aus.
