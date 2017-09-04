"""
Project:      Real Time Energy Consumption Forecasting System
Program:      prophet.py
Description:  
Made by:      Eirik Johannes Ramstad
Date:         03.09.2017
"""

from fbprophet import Prophet
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 


def nordpool():
    
    df = pd.read_csv('datasets/nordic_electricity_consumption_nordpool.csv', parse_dates=['Date'])
    
    area = 'NO'

    # Keep only relevant columns and format to what prophet expects
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

df = nordpool()

# Analyse data with prophet
m = Prophet(weekly_seasonality=True, yearly_seasonality=True)
m.fit(df)

# Make dataframe to hold forecast
future = m.make_future_dataframe(periods=730, freq='d')
future.tail()

forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

#print(forecast)

# Plot Results
m.plot(forecast)
plt.show()

# Plot Components will show the trend, yearly seasonality, weekly seasonality, 
m.plot_components(forecast)
plt.show()


