"""
Project:      Real Time Energy Consumption Forecasting System
Program:      prophet.py
Description:  
Made by:      Eirik Johannes Ramstad
Date:         28.08.2017
"""

from fbprophet import Prophet
import pandas as pd
import numpy as np


data = pd.read_csv('household_electricity_consumption.csv', parse_dates=[['Date', 'Time']])

# Keep only relevant columns and rename to what prophet expects

Global_active_power = data['time', 'Global_active_power']
df = Global_active_power.rename(columns={'time': 'df', 'Global_active_power': 'y'})

# Analyse data with prophet
m = Prophet()
m.fit(df)

# Make dataframe to hold forecast
future = m.make_future_dataframe(periods=365)
future.tail()

forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

# Plot Results
m.plot(forecast);

# Plot Components will show the trend, yearly seasonality, weekly seasonality, 
m.plot_components(forecast);
