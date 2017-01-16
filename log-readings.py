#!/usr/bin/env python
# -*- coding: utf-8 -*-


###############
# Get Sensors #
###############

import sensors

OneWireTemp = sensors.getOneWireReading()

humidity, temperature = sensors.getDHTReadings()

BMETemp, BMEPressure = sensors.getBMEReadings()

windspeed = sensors.getWindspeedReading()


###############
# Write to DB #
###############

# Connect

print "Connecting to DB..."

import sqlite3

sqlite_file = '/home/pi/weatherstation.db'
table_name = 'readings'

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()


# Write

rainfall = 0

print 'Temperature (onewire): %.2f' % (OneWireTemp)
print 'Temperature (DHT): %.2f' % (DHTTemp)
print 'Temperature (BMP): %.2f' % (BMETemp)
print 'Humidity: %.1f' % (humidity)
print 'Pressure: %.1f' % (BMEPressure)
print 'Windspeed %.1f' % (windspeed)
print 'Rainfall %.2f' % (rainfall) 

print "Writing to DB..."

c.execute("INSERT INTO READINGS (TIME,TEMPERATURE1, TEMPERATURE2, TEMPERATURE3,HUMIDITY,PRESSURE, WINDSPEED, RAINFALL) VALUES (CURRENT_TIMESTAMP, {temp1}, {temp2}, {temp3}, {humid}, {pressure}, {windspeed},0)".\
	format(temp1 = OneWireTemp, temp2 = BMETemp, temp3 = DHTTemp, pressure = BMEPressure, windspeed = windspeed, humid = humidity))

conn.commit()
conn.close()


#######################
# Write to thingspeak #
#######################

import paho.mqtt.publish as publish
import yaml
import ssl

with open("/home/pi/python-weather/config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

channelID = cfg['channelID']
apiKey = cfg['apiKey']

mqttHost = "mqtt.thingspeak.com"

tTransport = "websockets"
tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
tPort = 443
        
# Create the topic string
topic = "channels/" + channelID + "/publish/" + apiKey
    
# build the payload string
tPayload = "field1=" + str(OneWireTemp) + "&field2=" + str(BMETemp) + "&field3=" + str(DHTTemp) + "&field4=" + str(humidity) + "&field5=" + str(BMEPressure)  + "&field6=" + str(windspeed) + "&field7=" + str(rainfall)

# attempt to publish this data to the topic 
try:
    publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)

except Exception, e:
    print ("There was an error while publishing the data." + str(e))