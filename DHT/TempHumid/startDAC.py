import smbus
import time
import dht11
import RPi.GPIO as GPIO
import paho.mqtt.publish as publish
import psutil

#  ThingSpeak Channel Settings

# The ThingSpeak Channel ID
# Replace this with your Channel ID
channelID = "305122"

# The Write API Key for the channel
# Replace this with your Write API key
apiKey = "1NUYN01J6DD4W5KJ"

#  MQTT Connection Methods

# Set useUnsecuredTCP to True to use the default MQTT port of 1883
# This type of unsecured MQTT connection uses the least amount of system resources.
useUnsecuredTCP = False

# Set useUnsecuredWebSockets to True to use MQTT over an unsecured websocket on port 80.
# Try this if port 1883 is blocked on your network.
useUnsecuredWebsockets = False

# Set useSSLWebsockets to True to use MQTT over a secure websocket on port 443.
# This type of connection will use slightly more system resources, but the connection
# will be secured by SSL.
useSSLWebsockets = True


# Standard mqtt host
mqttHost = "mqtt.thingspeak.com"

# Set up the connection parameters based on the connection type
if useUnsecuredTCP:
    tTransport = "tcp"
    tPort = 1883
    tTLS = None

if useUnsecuredWebsockets:
    tTransport = "websockets"
    tPort = 80
    tTLS = None

if useSSLWebsockets:
    import ssl
    tTransport = "websockets"
    tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
    tPort = 443

# Create the topic string
topic = "channels/" + channelID + "/publish/" + apiKey

#define GPIO 14 as DHT11 data pin
Temp_sensor=4


#ENABLE = 0b00000100 # Enable bit
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1


def main():
  # Main program block
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  # Initialise display
  instance = dht11.DHT11(pin = Temp_sensor)

  while True:
	#get DHT11 sensor value
	result = instance.read()
    # Send some test

	if result.is_valid():
	    # build the payload string
	    tPayload = "field1=" + str(result.temperature) + "&field2=" + str(result.humidity)
	    # attempt to publish this data to the topic
	    try:
                publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)
            except (KeyboardInterrupt):
                break
            except:
                    print ("There was an error while publishing the data.")
	    print "temp:"+str(result.temperature)+" C"
	    print "humid:"+str(result.humidity)+"%"


# Set up the connection parameters based on the connection type
if useUnsecuredTCP:
    tTransport = "tcp"
    tPort = 1883
    tTLS = None

if useUnsecuredWebsockets:
    tTransport = "websockets"
    tPort = 80
    tTLS = None

if useSSLWebsockets:
    import ssl
    tTransport = "websockets"
    tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
    tPort = 443

# Create the topic string
topic = "channels/" + channelID + "/publish/" + apiKey


if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
   raise
