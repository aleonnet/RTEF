"""
Project: 		Real Time Energy Consumption Forecasting System
Program: 		forecaster.py
Description: 	Program to calculate forecast for energy consumption from MQTT stream 
				determined using a polynomial and publish the forecast to a new stream. 
Made by: 		Eirik Johannes Ramstad
Date:			28.08.2017
"""

# Imports
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import numpy
import time
import pylab

# Global Variables
polynomial = 6
arraysize = 10
xarray = numpy.arange(0,arraysize)
yarray = numpy.zeros(arraysize)
prevforecast = 0

# Callback for CONNACK response from server
def on_connect(self, client, userdata, rc):
    print("Connected with result code "+str(rc))
    self.subscribe("meters/lyse-test-01")


# Callback for PUBLISH message from server
def on_message(client, userdata, msg):
    print "---------------------------"
    global xarray, yarray, prevforecast
    
    # Format data
    print(msg.topic+" "+str(msg.payload))
    payload = json.loads(msg.payload)
    
    x = payload['timestamp']
    y = payload['value']
    
    # Basic statistics
    error = prevforecast - y
    print "Forecast: " + str(prevforecast) + " Actual: " + str(y) + " Error: " + str(error)

    # Calculate polynomial of new dataset
    yarray = numpy.roll(yarray,-1)
    yarray[9] = y
    print yarray 
    
    z = numpy.polyfit(xarray, yarray, 4)
    p = numpy.poly1d(z)
    yforecast = p(10)
    print "Forecasted Data: " + str(yforecast)

    payload['value'] = yforecast
    prevforecast = yforecast

    # Reformat data to json
    forecast = json.dumps(payload)

    # Publish forecast to MQTT 
    publish.single("predictions/lyse-test-01", forecast, hostname="127.0.0.1")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)

client.loop_forever()