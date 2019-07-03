import RPi.GPIO as gp
import paho.mqtt.client as mqtt
import time
import ssl

gp.setmode(gp.BOARD)
led=11
gp.setup(led,gp.OUT)
gp.output(led,0)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("led")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    data=msg.payload.decode("utf-8")
    print(data)
    if(data=="led on"):
        gp.output(led,1)
    elif(data=="led off"):
        gp.output(led,0)

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
client.loop_forever()
