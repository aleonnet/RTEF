# Real Time Energy Forecaster

## Description

The purpose of this application is to present a simple way to forecast future energy consumption based on a stream of MQTT data received from an electricity meter. The forecasted electricity consumption can then be used by a utility provider to better manage their electricity production. A better matched production vs. demand reduces the volatility of the electricity price, ultimately making electricity cheaper for the consumer. 


### How does it work?

The forecaster listens to a specified MQTT topic, calculates a forecast based on the received data and publishes its forecast to a second MQTT topic. The current program uses a fourth degree polynomial on the last five incoming datapoints to determine the forecast. 

The publisher has been made to simulate an electricity meter. It takes datapoints from a dataset and publishes it to an MQTT topic at a given time interval. 

The incoming data from the electricity meter is formatted using json and consists of a timestamp and value field. The output data from the forecaster is also formatted using json and consists of the future timestamp and future value.  


### Future improvements

* Use actual electricity consumption data to create relevant model

* Create a function to determine the accuracy of the forecast and make it easier to compare different models. 

* Add  time, weekday, date, temperature and daylight/weather-type variables to improve accuracy of a consumers forecast. 

* Use machine learning techniques on historic data from a large set of consumers to segment consumers based on their demand pattern, then develop models for each segment incorporating variables relevant to it. 


## Getting Started

### Prerequisites

For the forecaster to work, ensure that you use an appropriate computer with all the required dependencies installed. The Real Time Energy Forecaster was tested on a Fedora based Linux distribution using Python 2.7. The required dependencies can be found in the includes section of the programs.   


### Setting up local MQTT broker and subscriber

Start a local mosquitto broker by entering the following command into a terminal window:
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

The publisher app can be used to test the forecasting application. The publisher sends dummy data to the MQTT topic the forecaster is listening to. It can be run by entering the following command into a new terminal window. 
```
$ python publisher.py
```
A later release will include a function for evaluatating the acuracy of the forecasts and also include actual electricity consumption data to make it easier to determine the most suitable model for a given demand pattern.  

## License

This project is licensed under the [MIT License ](https://opensource.org/licenses/MIT)