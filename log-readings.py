import sqlite3
import random
import time

from Adafruit_BME280 import *

import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008



sensor = BME280(mode=BME280_OSAMPLE_8)

sqlite_file = '/home/pi/weatherstation.db'
table_name = 'readings'

# Connecting to the database file

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Get sensor readings form BPM208

degrees = sensor.read_temperature()
pascals = sensor.read_pressure()
hectopascals = pascals / 100
#humidity = sensor.read_humidity()







# Software SPI configuration:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

windChannel = 7

rawWindReading = mcp.read_adc(windChannel)

windspeedMetersPerSecond = rawWindReading




# Write to db

c.execute("INSERT INTO READINGS (TIME,TEMPERATURE,HUMIDITY,PRESSURE, WINDSPEED, RAINFALL) VALUES (CURRENT_TIMESTAMP, {temp}, 0, {pressure}, {windspeed}, 0)".\
	format(temp = degrees, pressure = hectopascals, windspeed = windspeedMetersPerSecond))

print windspeedMetersPerSecond
print "Sensor read"

conn.commit()
conn.close()