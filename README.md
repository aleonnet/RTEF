# Real Time Energy Forecaster

## Description

The purpose of this application is to forecast future energy consumption based on a stream of MQTT data received from an electricity meter. The forecasted electricity consumption can then be used by a utility provider to better manage their electricity production. A better matched production vs. demand reduces the volatility of the electricity price, ultimately making electricity cheaper and more reliable for the consumer. 


### How does it work?

The forecaster listens to a specified MQTT topic, calculates a forecast based on the received data and publishes its forecast to a second MQTT topic. The forecast is calculated based on previous data on top of a model generated using the timeseries forecasting tool [Prophet](https://github.com/facebookincubator/prophet) using 4.5 years worth of norwegian electricity consumption data taken from [Nordpool](https//www.nordpoolspot.com). A further explanation of the mathematics behind the forecasting can be found [here](). 

The publisher has been made to simulate an electricity meter. It takes datapoints from a dataset and publishes it to an MQTT topic at a given time interval. 

The incoming data from the electricity meter is formatted using json and consists of a timestamp and value field. The output data from the forecaster is also formatted using json and consists of the future timestamp and future value.


### Future improvements

* Implement prophet model into forecaster 

* Create a function to determine the accuracy of the forecast by comparing with actual data. 

* Add temperature and daylight/weather-type variables to further improve accuracy.


## Getting Started

### Prerequisites

For the forecaster to work, ensure that an appropriate computer with all the required dependencies installed is used. The Real Time Energy Forecaster has been tested using Python 2.7 on a computer running Ubuntu. The required dependencies can be found in the includes section of the programs. The Mosquitto message broker and clients also needs to be installed.


### Setting up a local MQTT broker and subscriber

Start a local mosquitto broker by entering the following command into a terminal window. Note, on some operating systems, this might not be necessary as it is already running in the background. 
```
$ mosquitto
```
Subscribe to the MQTT topic with the forecast outputs by opening a new terminal window and typing the following command:
```
$ mosquitto_sub -v -t 'predictions/test-01'
```

### Running the application

Run the forecasting application by entering the following command into a new terminal window:
```
$ python forecaster.py
```

The forecaster will now listen to the  MQTT topic specified in the program and output its calculated forecast to a second MQTT topic after every received message. 


## Testing the application

The publisher app can be used to test the forecasting application. The publisher sends electricity consumption data to the MQTT topic the forecaster is listening to. It can be run by entering the following command into a new terminal window. 
```
$ python publisher.py
```
A later release will include a function for evaluatating the acuracy of the forecasts to make it easier to determine the accuracy of the forecast and select the most suitable model for a given demand pattern.

The dataset has been sourced from [Nordpool](http://www.nordpoolspot.com) and contains daily sums of electric power consumption across the Nordic region from January 2013 to September 2017. 

## License

This project is licensed under the [MIT License ](https://opensource.org/licenses/MIT)


