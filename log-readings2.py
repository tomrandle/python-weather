#!/usr/bin/env python
# -*- coding: utf-8 -*-


import yaml

import sqlite3
import time


###############
# Get Sensors #
###############

import sensors


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

import paho.mqtt.publish as publish


with open("/home/pi/python-weather/config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

channelID = cfg['channelID']
apiKey = cfg['apiKey']
mqttHost = "mqtt.thingspeak.com"

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