#!/usr/bin/env python
# -*- coding: utf-8 -*-


##############
# DHT Sensor #
##############

import Adafruit_DHT


def getDHTReadings(): 

	DHTPin = 22

	DHTSensor = Adafruit_DHT.AM2302 

	print "Getting DHT sensor readings..."

	humidity, temperature = Adafruit_DHT.read_retry(DHTSensor, DHTPin)

	print humidity, temperature

	return humidity, temperature

#################
# BME280 Sensor #
#################

from Adafruit_BME280 import *

def getBMEReadings():

	BMPSensor = BME280(mode=BME280_OSAMPLE_8)

	print "Getting BMP Sensor readings..."

	# Get sensor readings form BPM208

	temperature = BMPSensor.read_temperature()
	pressure = BMPSensor.read_pressure() / 100 #mBar

	print temperature, pressure

	return temperature, pressure


###########
# MCP3008 #
###########

import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

def getWindspeedReading():

	# Software SPI configuration:
	CLK  = 18
	MISO = 23
	MOSI = 24
	CS   = 25

	print "Getting MCP3008 readings..."

	mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

	windChannel = 7

	rawWindReading = mcp.read_adc(windChannel)

	print rawWindReading

	# Convert wind voltage reading to speed (0.4-2V, 0 - 32.4 m/s)
	    
	windspeed = ((rawWindReading * 3.3 / 1024) - 0.4) * (32.4 / 1.6);

	if windspeed < 0:
		windspeed = 0

	return windspeed


###############################
# One wire Temperature sensor #
###############################

import os

def getOneWireReading():

	print "Getting 1wire reading..."
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


	temperature = read_temp()

	print temperature

	return temperature