# Set up BMP sensor

- Follow installation guide here `https://github.com/adafruit/Adafruit_Python_BME280/blob/master/Adafruit_BME280.py`. BME280 Adafruit python library works for BMP280 too.

## Wiring BMP280 Raspberry Pi Zero

![How to connect sensor to raspberry pi](https://cloud.githubusercontent.com/assets/895664/21616960/b296341a-d1db-11e6-8e45-9ac64f2c4b09.png "How to connect BMP280 to raspbery pi")

#Set up DHT sensor

Follow steps here: https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/software-install-updated

#Set up Analog to Digital converter

Follow steps here: https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008



#Set up 1-wire

(remember swapped pins to free up 4 for 1wire)
https://www.modmypi.com/blog/ds18b20-one-wire-digital-temperature-sensor-and-the-raspberry-pi





# Set up DB

- Set up sqlite db with following schema: 

	~~~~ 
	CREATE TABLE READINGS(
	ID INTEGER PRIMARY KEY,
	TIME           DATETIME    NOT NULL,
	TEMPERATURE    FLOAT,
	HUMIDITY       FLOAT,
	PRESSURE       FLOAT,
	WINDSPEED	  FLOAT,
	RAINFALL       FLOAT);
	~~~~

# Set up crontab

- Set up crontab with `sudo contab -e` => `* * * * * /usr/bin/python2.7 /home/pi/python-weather/log-readings.py`

#Notes 

- SSH problems fixed by: https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=142710
- Don't forget ; with SQLite
- Don't forget absolute file paths for everything when running cronjob

