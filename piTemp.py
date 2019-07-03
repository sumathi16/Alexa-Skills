import paho.mqtt.client as mqtt
import ssl
import Adafruit_DHT as d
from time import sleep
import sys
import json
import Adafruit_DHT

sensor=Adafruit_DHT.DHT11
pin=4
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
a="/home/pi/Downloads/ece/ece.pem"
b="/home/pi/Downloads/ece/e0d39b6a5b-certificate.pem.crt"
c="/home/pi/Downloads/ece/e0d39b6a5b-private.pem.key"
client.tls_set(ca_certs=a, certfile=b, keyfile=c, cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLS, ciphers=None)

client.connect("a1yms33ahy1eww-ats.iot.us-east-1.amazonaws.com", 8883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()

while 1:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        dat_in = {'temp':temperature,
                  'hum':humidity
                  }
        print(type(dat_in))

        dat_out = json.dumps(dat_in)
        print(type(dat_out))
        data = json.loads(dat_out)
        print(type(data))
        client.publish("temperature",dat_out,qos=1)
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity)                                                                                        )
    else:
        print('Failed to get reading. Try again!')


    #print("msg sent: temperature " + "%.2f" % k)
    #sleep(2)
