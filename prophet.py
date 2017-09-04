"""
Project:      Real Time Energy Consumption Forecasting System
Program:      prophet.py
Description:  Program to generate forecast on a dataset using 
              the prophet forecasting tool.
Made by:      Eirik Johannes Ramstad
Date:         03.09.2017
"""

from fbprophet import Prophet
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

# Functions to read csv and format dataframe into supported format
def nordpool():
    df = pd.read_csv('datasets/nordic_electricity_consumption_nordpool.csv', parse_dates=['Date'])
    
    area = 'NO3'

    df = df[['Date',area]]
    df = df.rename(columns={'Date': 'ds', area: 'y'})
    df = df.head(1705)
    
    return df


def dataset1():
    df = pd.read_csv('datasets/Apt1_2015.csv', parse_dates=['ds'])

    # Lowest granularity supported by prophet is days, so format data into days
    df = df.reset_index().set_index('ds').groupby(pd.TimeGrouper("d")).sum()
    df = df.reset_index()
    df = df[['ds','y']]

    df = df.head(346)

    return df

def dataset2():
    data = pd.read_csv('datasets/household_power_consumption.csv', parse_dates=[['Date', 'Time']])
    
    # Keep only relevant columns and format to what prophet expects
    df = data[['Date_Time','Global_active_power']]
    df = df.rename(columns={'Date_Time': 'ds', 'Global_active_power': 'y'})

    df = df.reset_index().set_index('ds').groupby(pd.TimeGrouper("d")).sum()
    df = df.reset_index()
    df = df[['ds','y']]

    return df

# Select data
df = nordpool()

# Analyse data with prophet
m = Prophet(weekly_seasonality=True, yearly_seasonality=True)
m.fit(df)

# Make dataframe and predict future values
future = m.make_future_dataframe(periods=730, freq='D')
forecast = m.predict(future)

# Plot Results
m.plot(forecast)
plt.title("Daily Electricity Consumption Forecast",fontsize=16)
plt.ylabel("Electricty Consumption (MWh)",fontsize=12)
plt.xlabel("Year",fontsize=12)
plt.show()

# Plot trend, yearly seasonality and weekly seasonality
m.plot_components(forecast)
plt.show()


