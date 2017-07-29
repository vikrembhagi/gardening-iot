import pigpio as gpio
import time
count = 0
value = 0
average = 0.00
flag=0
soil = gpio.pi()
soil.set_mode(17,gpio.INPUT)

def monitorSensor(reading):
    global count,value,average,flag
    count = count + 1
    value = value + float(reading)
    average = float(value/count)
    if average < 0.2:
        flag=1
        print flag
    print "This is the average"
    print average
    print type(reading)
    print value
    print count

while 1:
    print "#Buffer"
    print soil.read(17)
    time.sleep(1)
    monitorSensor(soil.read(17))



