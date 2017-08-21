import pigpio as gpio
import time
import tweet
count = 0
value = 0
average = 0.00
flag=0
soil = gpio.pi()
soil.set_mode(17,gpio.INPUT)

def monitorSensor(reading):
    global count,value,average,flag
    if ( reading == 1 ):
        tweet.sendAlert()
        
while 1:
    print "#Buffer"
    print soil.read(17)
    time.sleep(1800)
    monitorSensor(soil.read(17))



