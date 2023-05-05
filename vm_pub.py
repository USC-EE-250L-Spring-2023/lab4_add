"""EE 250L Lab 04 Starter Code
Run vm_sub.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time
from datetime import datetime
import socket # Publisher/MQTT Code
import RPi.GPIO as GPIO # Data Collection Init
#import matplotlib.pyplot as plt
import numpy as np

# HARDWARE INITIALIZATION: 
# Import SPI library (for hardware SPI) and MCP3008 library. (Data Collection)
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
    
GPIO.setmode(GPIO.BCM) # Use BCM Configuration
GPIO.setwarnings(False)

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# Set channels as outputs
led_pin = 17
GPIO.setup(led_pin, GPIO.OUT) # Set LED as an Output; BCM 17

"""This function (or "callback") will be executed when this client receives 
a connection acknowledgement packet response from the server. """
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))


if __name__ == '__main__':
    #get IP address
    ip_address=0 
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    # print(f"IP Address: {ip_address}") 
    
    #create a client object
    client = mqtt.Client()
    
    #attach the on_connect() callback function defined above to the mqtt client
    client.on_connect = on_connect
    """Connect using the following hostname, port, and keepalive interval (in 
    seconds). We added "host=", "port=", and "keepalive=" for illustrative 
    purposes. You can omit this in python. For example:
    
    `client.connect("eclipse.usc.edu", 11000, 60)` 
    
    The keepalive interval indicates when to send keepalive packets to the 
    server in the event no messages have been published from or sent to this 
    client. If the connection request is successful, the callback attached to
    `client.on_connect` will be called."""

    client.connect(host="broker.hivemq.com", port=1883, keepalive=60)

    """ask paho-mqtt to spawn a separate thread to handle
    incoming and outgoing mqtt messages."""
    client.loop_start()
    time.sleep(1)

    while True:
        #replace user with your USC username in all subscriptions
        client.publish("gtrue/ipinfo", f"{ip_address}")
        print("Publishing ip address")
        time.sleep(4)

        #get date and time 
        from datetime import date;
        today = date.today()
        ctime = datetime.now()
        
        #publish date and time in their own topics
        client.publish("gtrue/date", f"{today}")
        print("Publishing todays date")
        time.sleep(4)
        
        client.publish("gtrue/ctime", f"{ctime}")
        print("Publishing time")
        time.sleep(4)
