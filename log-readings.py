import sqlite3
import time

##############
# DHT Sensor #
##############

import Adafruit_DHT

DHTSensor = Adafruit_DHT.DHT11 #DHT22 when switch sensor

DHTPin = 4

humidity, temperature = Adafruit_DHT.read_retry(DHTSensor, DHTPin)


#################
# BME280 Sensor #
#################

from Adafruit_BME280 import *

sensor = BME280(mode=BME280_OSAMPLE_8)

# Get sensor readings form BPM208

degrees = sensor.read_temperature()
pascals = sensor.read_pressure()
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


###############
# Write to DB #
###############

# Connect to the database file

sqlite_file = '/home/pi/weatherstation.db'
table_name = 'readings'

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()


# Write to db

c.execute("INSERT INTO READINGS (TIME,TEMPERATURE,HUMIDITY,PRESSURE, WINDSPEED, RAINFALL) VALUES (CURRENT_TIMESTAMP, {temp}, {humid}, {pressure}, {windspeed}, 0)".\
	format(temp = temperature, pressure = hectopascals, windspeed = windspeedMetersPerSecond, humid = humidity))

print windspeedMetersPerSecond, temperature, humidity
print "Sensor read"

conn.commit()
conn.close()