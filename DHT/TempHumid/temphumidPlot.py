#
# pull data from sql, plot using matplotlib
# see http://stackoverflow.com/questions/18663746/matplotlib-multiple-lines-with-common-date-on-x-axis-solved
#
# rev 1.0 12/02/2013 WPNS built from GraphAirmuxSD.py V1.1
# rev 1.1 12/02/2013 WPNS remove large delta values
# rev 1.2 12/02/2013 WPNS remove -0.1 values (failed to read)
# rev 1.3 12/02/2013 WPNS show count of anomalies
# rev 1.4 12/03/2013 WPNS cleanup, release
# rev 1.5 12/03/2013 WPNS better label
# rev 1.6 12/03/2013 WPNS bugfix, release
# rev 1.69 12/04/2013 WPNS release to Instructables

import sys
import os
import time
import math
import datetime
import MySQLdb as mdb
import numpy

# so matplotlib has to have some of the setup parameters _before_ pyplot
import matplotlib
matplotlib.use('agg')

#matplotlib.rcParams['figure.dpi'] = 100
#matplotlib.rcParams['figure.figsize'] = [10.24, 7.68]
matplotlib.rcParams['lines.linewidth'] = 0.5
matplotlib.rcParams['axes.color_cycle'] = ['r','g','b','k']
matplotlib.rcParams['axes.labelsize'] = 'large'
matplotlib.rcParams['font.size'] = 8
matplotlib.rcParams['grid.linestyle']='-'

import matplotlib.pyplot as plt

anomalies = 0

print "TempHumidPlot.py V1.69 12/04/2013 WPNS",time.asctime(),

# open the database connection, read the last <many> seconds of data, put them in a Numpy array called Raw
pwd = "P@$$w0rd!"
DBconn = mdb.connect(host="localhost",user="root",passwd=pwd,db="temphumid_database")
cursor = DBconn.cursor()
sql = "select datetime,temperature,humidity from temphumidLog"
#where datetime >= (unix_timestamp(now())-(60*60*24))"
cursor.execute(sql)
Raw = numpy.fromiter(cursor.fetchall(), count=-1, dtype=[('','<M8[us]'),('temp',numpy.int8),('humid',numpy.int8)])
Raw = Raw.view(dtype='M8[us],int8,int8').reshape(-1, len(Raw))
print Raw
(samples,ports)=Raw.shape
print 'Samples: {}, DataPoints: {}'.format(samples,ports),
plotme=numpy.zeros((samples,ports-1)) # make an array the same shape minus the epoch numbers



for y in range(ports-1):
#    print y
    for x in range(samples-1):  # can't do last one, there's no (time) delta from previous sample
        seconds = Raw[x+1,0]-Raw[x,0]
        # if the number didn't overflow the counter
        plotme[x,y] = Raw[x,y+1]

    plotme[samples-1,y] = None # set last sample to "do not plot"

    for x in range(samples-1):                   # go thru the dataset again
        if (Raw[x+1,1] == -0.1):                 # if values are "reading failed" flag
            plotme[x+1,0] = plotme[x,0]          # copy current sample over it
            plotme[x+1,1] = plotme[x,1]          # for temperature and humidity both
            anomalies += 1

        if (abs(Raw[x+1,1]-Raw[x,1]) > 10):      # if temperature jumps more than 10 degrees in a minute
            plotme[x+1,0] = plotme[x,0]          # copy current sample over it
            plotme[x+1,1] = plotme[x,1]          # for temperature and humidity both
            anomalies += 1

print "Anomalies: ",anomalies,

#print plotme

# get an array of adatetime objects (askewchan from stackoverflow, above)
dts = map(datetime.datetime.fromtimestamp, Raw[:,0])

# set up the plot details we want
plt.grid(True)
plt.ylabel('Temp C, RH %%')
plt.axis(ymax=100,ymin=0)
plt.xlabel(time.asctime())
plt.title("<location_name> Temperature (Red), Humidity (Green)")
plt.hold(True)

# and some fiddly bits around formatting the X (date) axis
plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m/%d %H:%M'))
plt.gca().xaxis.set_major_locator(matplotlib.dates.HourLocator())
lines = plt.plot(dts,plotme)
plt.gcf().autofmt_xdate()

FileName = '/home/pi/PiDAC/DHT/TempHumid/Graphs/TH.png'
plt.savefig(FileName)

#print 'Copy to Web Server...',
#Destination = '/var/www/'
#os.system("cp /root/Graph/graphics/TH.png {}".format(Destination))
#print 'Done at',time.asctime()
#