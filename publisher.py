"""
Project: 		Real Time Energy Consumption Forecasting System
Program: 		publisher.py
Description: 	Program to publish energy consumption data to a locally hosted MQTT server
Made by: 		Eirik Johannes Ramstad
Date:			28.08.2017

"""

# Imports
import json
import time
import numpy

# Test datasets
data1 = numpy.arange(0,20)
data2 = [0,1,4,9,16,25,36,49,64,81,100]
data3 = [0,3,9,27,81,27,9,3,0]

# Send 10 packets
for x in range(0,10):

    pydict = {'timestamp':'2017-07-28T12:49:12.468207', 'value':data3[x]}
    dict2json = json.dumps(pydict)

    command = "mosquitto_pub -t 'meters/lyse-test-01' -m '"+ str(dict2json) +"'"
    subprocess.check_output(["bash", '-c',command])

    print('Data Sent!')
    time.sleep(1)

