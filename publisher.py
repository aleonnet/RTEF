"""
Project:        Real Time Energy Consumption Forecasting System
Program:        publisher.py
Description:    Program to publish energy consumption data to a locally hosted MQTT broker
Made by:        Eirik Johannes Ramstad
Date:           28.08.2017

"""

# Imports
import json
import time
import datetime
import numpy
import subprocess
import pandas as pd


df = pd.read_csv('datasets/nordic_electricity_consumption_nordpool.csv')#, parse_dates=['Date'])
df = df.tail(976)

for index, row in df.iterrows():
    
    pydict = {'timestamp':row['Date'], 'value':row['NO']} 

    dict2json = json.dumps(pydict)

    command = "mosquitto_pub -t 'meters/test-01' -m '"+ str(dict2json) +"'"
    subprocess.check_output(["bash", '-c',command])

    print(row['Date'] + ' -- Data sent!')
    time.sleep(30)



