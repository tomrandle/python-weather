import sqlite3
import time

from Adafruit_BME280 import *

import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

import Adafruit_DHT




# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHTSensor = Adafruit_DHT.DHT11

# Example using a Beaglebone Black with DHT sensor
# connected to pin P8_11.
# pin = 'P8_11'

# Example using a Raspberry Pi with DHT sensor
# connected to GPIO23.
DHTPin = 4

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(DHTSensor, DHTPin)






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

c.execute("INSERT INTO READINGS (TIME,TEMPERATURE,HUMIDITY,PRESSURE, WINDSPEED, RAINFALL) VALUES (CURRENT_TIMESTAMP, {temp}, {humid}, {pressure}, {windspeed}, 0)".\
	format(temp = temperature, pressure = hectopascals, windspeed = windspeedMetersPerSecond, humid = humidity))

print windspeedMetersPerSecond, temperature, humidity
print "Sensor read"

conn.commit()
conn.close()