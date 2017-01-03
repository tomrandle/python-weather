import sqlite3
import random
import time

from Adafruit_BME280 import *

sensor = BME280(mode=BME280_OSAMPLE_8)

sqlite_file = '../test.db'
table_name = 'readings'

# Connecting to the database file

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Get sensor readings form BPM208

degrees = sensor.read_temperature()
pascals = sensor.read_pressure()
hectopascals = pascals / 100
#humidity = sensor.read_humidity()

# Write to db

c.execute("INSERT INTO READINGS (TIME,TEMPERATURE,HUMIDITY,PRESSURE, WINDSPEED, RAINFALL) VALUES (CURRENT_TIMESTAMP, {temp}, 0, {pressure}, 0, 0)".\
	format(temp = degrees, pressure = hectopascals))

time.sleep(10)
conn.commit()
conn.close()