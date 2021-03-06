import paho.mqtt.client as mqtt
import json, sched, time
import threading
import create, sw_song
import urllib2

# user parameters to configure before use

MQTT_broker = "192.168.1.18"
MQTT_Port = 1883
MQTT_User = "gladys_admin"
MQTT_PW = "Pa!ate"

DD_pin = 18

#  end of user parameters


delay = 1
des_delay = 10
bat_stop = 5
bat_base = 15
status = 0

s = sched.scheduler(time.time, time.sleep)
def print_status(C, s):
	global status
	global delay
	senses = robot.sensors([create.BATTERY_CHARGE, create.BATTERY_CAPACITY,create.CURRENT])
	bat_stat = (senses[create.BATTERY_CHARGE]*100)/senses[create.BATTERY_CAPACITY]
	print ("battery:")
	print bat_stat
	robot.printSensors() # debug output
	print ("delay:")
	print delay
	print ("for:")
	print des_delay
	
	if senses[create.BATTERY_CAPACITY]>= -1000:
		status=0
	else:
		status=1
	
	if delay >= des_delay:
		pld = "{\"_type\":\"stat\",\"power\":\"%d\",\"batt\":\"%d\"}" % (status,bat_stat,)
		C.publish("roomba/stat/", payload=pld, qos=0, retain=False)
		delay = 1
	else:
		delay += 1
		
	if status == 1:
		if bat_stat < bat_stop:
			robot.toPowerMode()
			status = 0
		else:
			if bat_stat < bat_base:
				robot.toBaseMode()
				status = 0

	s.enter(30,1,print_status,(C,s,))

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected to broker with result code "+str(rc))
	
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe("roomba/cmd")
	t_cyclic.start()
	
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	global status
	global des_delay
	print ("received message from broker" + msg.payload)
	data = json.loads(msg.payload)
	typ = data["_type"]
	if typ == 'cmd':

                power = data["power"]
#	        mode = data["mode"] for futur use
                print ("powering:"+power)
                if power == '1':
                	robot.toCleanMode()
                	status = 1
                	des_delay = 10
                else:
                	robot.toPowerMode()
#			robot.toBaseMode()
                	status = 0
                	des_delay = 60
	
	if typ == 'ping':
		robot.toSafeMode()
                sw_song.play_starwars(robot)
		robot.toSafeMode()
	
	print robot.getMode()

# The callback for when the client receives a disconnect response from the server
def on_disconnect(client, userdata, rc):
        if rc !=0:
                print("Disconnected from broker, reconnecting...")
                client.reinitialise()
                client.connect(MQTT_broker, MQTT_Port, 60)
        
	
def connect_roomba():

	print ("connected to roomba")	
	robot.toSafeMode()
	print ("roomba ready in safeMode")

def wait_for_internet_connection():
	print("Waiting for connection")
	while True:
		try:
			time.sleep(1)
           		response = urllib2.urlopen('https://www.google.fr/',timeout=1)
			return
		except urllib2.URLError:
			pass

wait_for_internet_connection()
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.username_pw_set(MQTT_User, password=MQTT_PW)
#s.enter(3,1,print_status,(client,s,))

robot = create.Create('/dev/serial0',DD_pin)

status = 0

# Start a thread to run the events
t_cyclic = threading.Thread(target=s.run)

t_roomba = threading.Thread(target=connect_roomba())
t_roomba.start()

t_receiver = threading.Thread(target=client.connect(MQTT_broker, MQTT_Port, 60))
t_receiver.start()

print_status(client,s)

try:
        print ("loop")

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        client.loop_forever()

#except KeyboardInterrupt:
        #quiting nicely

#except:

finally:
        client.disconnect()
        
        robot.close()
        
        


