import Adafruit_DHT

def getReadings():

	DHTSensor = Adafruit_DHT.AM2302 
	DHTPin = 22

	print "Getting DHT sensor readings..."

	humidity, temperature = Adafruit_DHT.read_retry(DHTSensor, DHTPin)

	return humidity, temperature