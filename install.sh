#git clone https://github.com/eclipse/paho.mqtt.python
#cd paho.mqtt.python
#python setup.py install

(crontab -l 2>/dev/null; echo "@reboot python /home/pi/roomba_drive/roomba/mqtt.py > /home/pi/roomba_drive/logs.log 2>&1") | crontab -

#sudo mv ./root /var/spool/cron/crontabs/root

#crontab -l > mycron
#echo "@reboot python /home/pi/roomba_drive/roomba/mqtt.py > /home/pi/roomba_drive/logs.log 2>&1" >> mycron
#crontab mycron
#rm mycron