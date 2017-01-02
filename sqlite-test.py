import sqlite3
import random
import time

sqlite_file = '../test.db'
table_name = 'readings'

# Connecting to the database file

while True:

	conn = sqlite3.connect(sqlite_file)

	c = conn.cursor()


	c.execute("INSERT INTO READINGS (TIME,TEMPERATURE,HUMIDITY,PRESSURE, WINDSPEED, RAINFALL) VALUES (CURRENT_TIMESTAMP, {temp}, 0, 0, 0, 0)".\
		format(temp=random.randint(1, 100)))


	 # c.execute("INSERT INTO {tn} ({idf}, {cn}) VALUES (123456, 'test')".\
	 #        format(tn=table_name, idf=id_column, cn=column_name))

	time.sleep(10)
	conn.commit()
	conn.close()



# INSERT INTO READINGS (TIME,TEMPERATURE,HUMIDITY,PRESSURE, WINDSPEED, RAINFALL)
# VALUES (CURRENT_TIMESTAMP, 4, 99, 1000, 0, 0);


