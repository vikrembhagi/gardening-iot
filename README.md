## Setup
To run code make sure you have:

1. Python 3
2. Pip
3. (For sensor code) : Raspberry Pi

Start by installing all the required packages through pip :

_pip install -r requirements.txt_

To use functionality, simply run the files.

## Hardware

1. Soil Sensor from this kit: http://a.co/aErkzJ9 (Amazon link for osoyoo sensor kit). The soil sensor is one amongst many..

## Files and functionality

On Raspberry Pi:

Start the pigpio server: _sudo pigpiod_

1. Recording and reporting soil moisture sensor recordings on raspberry pi : SoilMoisture2/Alternate.py : 
2. Send tweet : tweet.py

Change:

1. Add your own twitter bots credentials and message in tweet.py file
