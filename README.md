# Setup 

- Follow installation guide here `https://github.com/adafruit/Adafruit_Python_BME280/blob/master/Adafruit_BME280.py`. BME280 Adafruit python library works for BMP280 too.
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

- Set up crontab with `sudo contab -e` => `* * * * * /usr/bin/python2.7 /home/pi/python-weather/log-readings.py`


## Wiring BMP280 Raspberry Pi Zero

![How to connect sensor to raspberry pi](https://cloud.githubusercontent.com/assets/895664/21616960/b296341a-d1db-11e6-8e45-9ac64f2c4b09.png "How to connect BMP280 to raspbery pi")

#Notes 

- SSH problems fixed by: https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=142710
- Don't forget ; with SQLite
- Don't forget absolute file paths for everything when running cronjob
