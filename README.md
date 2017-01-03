# Notes

- Set up sqlite db first
- BME280 Adafruit python library works for BMP280 too
- SSH problems fixed by: https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=142710
- Don't forget ; with SQLite
- Don't forget absolute file paths for everything when running cronjob
-


	~~~~ 
	CREATE TABLE READINGS(
   ID INTEGER PRIMARY KEY,
   TIME           DATETIME    NOT NULL,
   TEMPERATURE    FLOAT,
   HUMIDITY       FLOAT,
   PRESSURE       FLOAT,
   WINDSPEED	  FLOAT,
   RAINFALL       FLOAT
);
	~~~~