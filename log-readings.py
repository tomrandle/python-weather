#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sqlite3
import time
import os

##############
# DHT Sensor #
##############

import Adafruit_DHT

DHTSensor = Adafruit_DHT.DHT11 #DHT22 when switch sensor

DHTPin = 22

humidity, temperature = Adafruit_DHT.read_retry(DHTSensor, DHTPin)


#################
# BME280 Sensor #
#################

from Adafruit_BME280 import *

BMPSensor = BME280(mode=BME280_OSAMPLE_8)

# Get sensor readings form BPM208

degrees = BMPSensor.read_temperature()
pascals = BMPSensor.read_pressure()
hectopascals = pascals / 100
#humidity = sensor.read_humidity()


###########
# MCP3008 #
###########

import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Software SPI configuration:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25

mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

windChannel = 7

rawWindReading = mcp.read_adc(windChannel)

windspeedMetersPerSecond = rawWindReading

###########
# One wire Temperature sensor #
###########

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


temp_sensor = '/sys/bus/w1/devices/28-00000556acc0/w1_slave'

def temp_raw():
	f = open(temp_sensor, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():

	lines = temp_raw()
	
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = temp_raw()
		temp_output = lines[1].find('t=')

		if temp_output != -1:
			print 'found temp'
			temp_string = lines[1].strip()[temp_output+2:]
			print temp_string
			temp_c = float(temp_string) / 1000.0
			return temp_c


OneWireTemp = read_temp()
print OneWireTemp


###############
# Write to DB #
###############

# Connect

sqlite_file = '/home/pi/weatherstation.db'
table_name = 'readings'

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()


# Write

c.execute("INSERT INTO READINGS (TIME,TEMPERATURE,HUMIDITY,PRESSURE, WINDSPEED, RAINFALL) VALUES (CURRENT_TIMESTAMP, {temp}, {humid}, {pressure}, {windspeed}, 0)".\
	format(temp = OneWireTemp, pressure = hectopascals, windspeed = windspeedMetersPerSecond, humid = humidity))

print windspeedMetersPerSecond, temperature, humidity
print "Sensor read"

conn.commit()
conn.close()