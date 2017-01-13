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

	x = lines[1].split("t=")
	
	temp_c = float(x[1]) / 1000.0
	
	return temp_c


OneWireTemp = read_temp()


###############
# Write to DB #
###############

# Connect

sqlite_file = '/home/pi/weatherstation.db'
table_name = 'readings'

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()


# Write



rainfall = 0

print 'Temperature (onewire): %.2f\nTemperature (DHT): %.2f\nTemperature (BMP): %.2f\n Humidity: %.1f\n Pressure: %.1f\n Windspeed %.1f\n Rainfall %.2f' % (OneWireTemp, temperature, degrees, humidity, hectopascals, windspeedMetersPerSecond, rainfall) 


c.execute("INSERT INTO READINGS (TIME,TEMPERATURE1, TEMPERATURE2, TEMPERATURE3,HUMIDITY,PRESSURE, WINDSPEED, RAINFALL) VALUES (CURRENT_TIMESTAMP, {temp1}, {temp2}, {temp3}, {humid}, {pressure}, {windspeed},0)".\
	format(temp1 = OneWireTemp, temp2 = degrees, temp3 = temperature, pressure = hectopascals, windspeed = windspeedMetersPerSecond, humid = humidity))

conn.commit()
conn.close()

