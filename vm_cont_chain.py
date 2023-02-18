"""EE 250L Lab 04 PART 2"""

import paho.mqtt.client as mqtt
import socket
import time


def on_connect(client, userdata, flags, rc):
    # Subscribe to servers
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("gtrue/ping")
    
    #Add the custom callbacks by indicating the topic and the name of the callback handle
    client.message_callback_add("gtrue/ping", call_back_ping)
   
def call_back_ping(client, userdata, message):
    num = int(message.payload.decode()) + 1
    print(num) 
    time.sleep(1)
    client.publish("gtrue/pong", num)
    print("Ponging Num!")
      
def on_message(client, userdata, msg):
    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))

if __name__ == '__main__':
    #create a client object
    client = mqtt.Client()
    #attach a default callback which we defined above for incoming mqtt messages
    client.on_message = on_message
    #attach the on_connect() callback function defined above to the mqtt client
    client.on_connect = on_connect

          
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    
    client.loop_forever()
   
        
