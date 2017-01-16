#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from __future__ import print_function
import paho.mqtt.publish as publish

import yaml


import sqlite3
import time



import getReadings


humidity, temperature = sensors.getDHTReadings()

degrees, hectopascals = sensors.getBMEReadings()

windspeedMetersPerSecond = sensors.getWindspeedReading()

OneWireTemp = sensors.getOneWireReading()


###############
# Write to DB #
###############

# Connect

print "Connecting to DB..."

sqlite_file = '/home/pi/weatherstation.db'
table_name = 'readings'

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()


# Write

rainfall = 0

print 'Temperature (onewire): %.2f' % (OneWireTemp)
print 'Temperature (DHT): %.2f' % (temperature)
print 'Temperature (BMP): %.2f' % (degrees)
print 'Humidity: %.1f' % (humidity)
print 'Pressure: %.1f' % (hectopascals)
print 'Windspeed %.1f' % (windspeedMetersPerSecond)
print 'Rainfall %.2f' % (rainfall) 

print "Writing to DB..."

c.execute("INSERT INTO READINGS (TIME,TEMPERATURE1, TEMPERATURE2, TEMPERATURE3,HUMIDITY,PRESSURE, WINDSPEED, RAINFALL) VALUES (CURRENT_TIMESTAMP, {temp1}, {temp2}, {temp3}, {humid}, {pressure}, {windspeed},0)".\
	format(temp1 = OneWireTemp, temp2 = degrees, temp3 = temperature, pressure = hectopascals, windspeed = windspeedMetersPerSecond, humid = humidity))

conn.commit()
conn.close()


#######################
# Write to thingspeak #
#######################



with open("/home/pi/python-weather/config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)


###   Start of user configuration   ###   

#  ThingSpeak Channel Settings

# The ThingSpeak Channel ID
# Replace this with your Channel ID
channelID = cfg['channelID']

# The Write API Key for the channel
# Replace this with your Write API key
apiKey = cfg['apiKey']

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

###   End of user configuration   ###

# The Hostname of the ThinSpeak MQTT service
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

    
# build the payload string
tPayload = "field1=" + str(OneWireTemp) + "&field2=" + str(degrees) + "&field3=" + str(temperature) + "&field4=" + str(humidity) + "&field5=" + str(hectopascals)  + "&field6=" + str(windspeedMetersPerSecond) + "&field7=" + str(rainfall)

# attempt to publish this data to the topic 
try:
    publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)

except Exception, e:
    print ("There was an error while publishing the data." + str(e))





