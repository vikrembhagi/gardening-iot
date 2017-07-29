import smbus
import time
import dht11
import RPi.GPIO as GPIO
import MySQLdb
import psutil



#define GPIO 14 as DHT11 data pin
Temp_sensor=4

#Variables for MySQL
pwd = "P@$$w0rd!"
db = MySQLdb.connect(host="localhost",user="root",passwd=pwd,db="temphumid_database")
cur = db.cursor()

#ENABLE = 0b00000100 # Enable bit
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1


def main():
  # Main program block
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  # Initialise display
  instance = dht11.DHT11(pin = Temp_sensor)

  while True:
	#get DHT11 sensor value
	result = instance.read()

    # Send some test

	if result.is_valid():
	    datetimeWrite = time.strftime("%y-%m-%d ")+time.strftime("%H:%M:%S")
	    temper = result.temperature
	    print temper
	    humid = result.humidity
	    print humid
	    print "temp:"+str(result.temperature)+" C"
	    print "humid:"+str(result.humidity)+"%"
	    print datetimeWrite

	    sql = ("""INSERT INTO temphumidLog (datetime,temperature,humidity) VALUES (%s,%s,%s)""",(datetimeWrite,temper,humid))
	    #sql = ("""INSERT INTO temphumidLog (datetime,temperature,humidity) VALUES (%s,%s,%s)""",('2017-07-21 12:55:23',25,57))
	    try:
	        print "Writing to database..."
	        #Execute the SQL command
	        cur.execute(*sql)
	        #Commit your changes in the database
	        db.commit()
	        print "Write Complete"

	    except:
	         #rollback in case there is an error
	         db.rollback()
	         print "Failed writing to database"

	    cur.close()
	    db.close()
	    break


if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
   raise
