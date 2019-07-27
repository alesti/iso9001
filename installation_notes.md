# Hard- und Software Installationsnotizen
## Installation Suffkopp (raspi)

[Raspbian Buster Lite](https://www.raspberrypi.org/downloads/raspbian/)
mit Etcher. 

* raspi-config: SSH angeklemmt, Wlan, Lokalisierung, alle Schnittstellen
erstmal an.
* Accounts angelegt (aleks, sudo), cocktail für den ganzen
  Scheiss. pi = /bin/false, sshd only publickey-auth only, pi pw gescrambled.
* cocktail in die wesentlichen Gruppen gestopft
* Zusätzliche Packages: `etckeeper, git, vim, screen, python3-dev, python3-pip, python3-smbus, i2c-tools, python3-rpi.gpio`

### Kivy Installation

Als User cocktail - so wie es da steht.
Examples wohnen in `~/.local/share/kivy-examples/demo/showcase`

### Hector Installation
`git clone https://github.com/H3c702/Hector9000.git`

`pip3 install --user -r requirements.txt`

## Adafruit PCA9685 Servo Driver

Wie anschliessen? 

https://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi/configuring-your-pi-for-i2c

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
https://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi/hooking-it-up
https://cdn-learn.adafruit.com/assets/assets/000/069/564/original/components_raspi_pca9685_i2c_with_servo.jpg?1547757668

vs. Laut Doku: Erstmal RASPI BCM2 (Pin 3) => PCA9685 SDA; RASPI BCM 3 (Pin 5) => PCA9685 SCL.
5V vom Netzteil.

## Relais für Pumpe und Zeug
Besser mit Treiber:
http://www.susa.net/wordpress/2012/06/raspberry-pi-relay-using-gpio/

https://indibit.de/raspberry-pi-gpio-ausgaenge-schalten-eingaenge-lesen/#Ausgang_schalten

## ATX Netzteil 

Ist genormt, siehe [PSU as workbench supply](https://www.electronics-tutorials.ws/blog/convert-atx-psu-to-bench-supply.html):

Farbe | PIN | Spannung | 24 Molex / Info
----- | --- | ---- | ----
orange | 1, 2, 12, 13 | 3,3V |
rot| 4, 6, 21, 22, 23 |5V | 
grau | 8 | 5V | wenn PSU ok
lila| 9 | 5V | standby
gelb| 10, 11 | 12V|
blau| 14 | -12V|
grün| 16 | 5V switch on| auf Masse ziehen
weiss | 20 | -5V |
schwarz| common | Masse|

Um das Netzteil ohne Motherboard zu benutzen, PIN16 auf Masse ziehen (vielleicht mit einem gut erreichbaren Schalter, aber der eigentliche Netzteilschalter ist das ja auch.
Das Netzteil braucht eine (geringe) Grundlast. LED mit 220Ohm Vorwiderstand an PIN8 nach Masse - oder eben Hector.

