"""
Project:        Real Time Energy Consumption Forecasting System
Program:        publisher.py
Description:    Program to publish energy consumption data to a locally hosted MQTT server
Made by:        Eirik Johannes Ramstad
Date:           28.08.2017

"""

# Imports
import json
import time
import datetime
import numpy
import subprocess

# Test datasets
data2 = numpy.arange(0,20)
data1 = [0,1,4,9,16,25,36,49,64,81,100,11*11,12*12,13*13,14*14,15*15,14*14,13*13,12*12,11*11,100,81,64,49,36,25,16,9,4,1]

# Send 60 packets
for x in range(0,60):
	# Get time
    now = datetime.datetime.now()
    timeString = now.strftime("%d.%m.%Y %H:%M:%S")

    data1 = numpy.roll(data1,-1)

    pydict = {'timestamp':timeString, 'value':data1[0]}    
    dict2json = json.dumps(pydict)

    command = "mosquitto_pub -t 'meters/test-01' -m '"+ str(dict2json) +"'"
    subprocess.check_output(["bash", '-c',command])

    print(timeString + ' -- Data sent!')
    time.sleep(1)

