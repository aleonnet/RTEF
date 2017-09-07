"""
Project:      Real Time Energy Consumption Forecasting System
Program:      forecaster.py
Description:  Program to calculate forecast of energy consumption from an MQTT topic 
              determined using a polynomial and publish the forecast to a new topic. 
Made by:      Eirik Johannes Ramstad
Date:         28.08.2017
"""

# Imports
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import numpy
import time
import datetime


# Global Variables
polynomialfactor = 4
arraysize = 5
interval = 1 # (seconds)
xarray = numpy.arange(0,arraysize)
yarray = numpy.zeros(arraysize)
prevforecast = 0

# Forecast calculations
def polynomial(newData):
    global xarray, yarray, prevforecast, arraysize, interval, polynomialfactor
    
    forecastData = {'timestamp':"",'value':0.}
    x = newData['timestamp']
    y = newData['value']
    
    # Basic statistics
    error = prevforecast - y
    print("Previous forecast: " + str(prevforecast) + " Actual: " + str(y) + " Error: " + str(error))

    # Calculate polynomial of new dataset
    yarray = numpy.roll(yarray,-1)
    yarray[arraysize-1] = y
    
    #xarray = numpy.roll(xarray,-1) # Need to use timestamps instead
    #xarray[arraysize-1] = x

    z = numpy.polyfit(xarray, yarray, polynomialfactor)
    p = numpy.poly1d(z)
    yforecast = p(arraysize) # Use timestamp + interval

    now = datetime.datetime.now() # Cheating, should use received timestamp
    forecastTime = now + datetime.timedelta(0,interval)
    forecastTimeStr = forecastTime.strftime("%d.%m.%Y %H:%M:%S")

    print("New forecast: " + str(yforecast) + " At time: " + forecastTimeStr)
 
    forecastData['timestamp'] = forecastTimeStr
    forecastData['value'] = yforecast

    prevforecast = yforecast

    return forecastData


# Callback for CONNACK response from server
def on_connect(self, client, userdata, rc):
    print("Connected with result code "+str(rc))
    self.subscribe("meters/test-01")


# Callback for PUBLISH message from server
def on_message(client, userdata, msg):
    print("--------------------------------------------------------")
    print("Received data: " + msg.topic + " " + str(msg.payload))

    # Format data
    payload = json.loads(msg.payload.decode('utf-8'))

    # Calculate forecast
    #payload = polynomial(payload)
    payload = prophet(payload)    

    # Reformat data to json
    forecast = json.dumps(payload)

    # Publish forecast to MQTT 
    publish.single("predictions/test-01", forecast, hostname="127.0.0.1")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)

client.loop_forever()

