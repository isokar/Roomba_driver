# Roomba-Driver

Python App to control Roomba robot with a Rpi via MQTT protocol

Compatible with Gladys-Roomba hook
Need paho.mqtt.client library

## Documentation

### Software installation

To install this module, simply launch the install.sh script.
it will automaticaly download libraries and configure what's need to be done(crontab...).
Don't forget to open and modify MQTT.py to adapt with your configuration(mostly for MQTT parameters).
The script will reboot your Pi at the end, It should be good.


### Hardware installation

To communicate with Roomba, you need to plug your Pi serial interface through a converter as Roomba works with 5V signals and Pi works with 3.3V.

![Roomba Pinout](https://www.google.fr/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=0ahUKEwiCs4bCwdnYAhWF1xQKHf9aC1UQjhwIBQ&url=https%3A%2F%2Fwww.eevblog.com%2Fforum%2Fbeginners%2Fmini-din-7-pcb-headerroomba-wifi%2F&psig=AOvVaw2DUZMnu2EB_4VXH2oA9HpR&ust=1516089979213768 "Roomba Pinout")

4 signals are needed:

|Pi       |    |  Roomba|
|-------  |--- |--------|
|TX  - 8  | -> |  3 - RX|
|RX  - 10 | <- |  4 - TX|
|DD  - 24 | -> | 5 - DD*|
|GND - 6  | <> | 6 - GND|

**DD(Device Detect) can be plugged on any other GPIO, just modify it on MQTT.py file*

WARNING!!: You can use the power from Roomba(Pin 1 & 2) but you have to use a voltage regulator as it is an unregulated voltage directly from battery. It can raise at more than 20V during charges.

