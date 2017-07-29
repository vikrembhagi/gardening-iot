
import pandas as pd
import sys
import os
import time
import math
import datetime
import MySQLdb as mdb
import numpy
import matplotlib.pyplot as plt
import pylab
import matplotlib.dates as mdates

print "TempHumidPlot.py V1.69 12/04/2013 WPNS",time.asctime(),

# open the database connection, read the last <many> seconds of data, put them in a Numpy array called Raw
pwd = "P@$$w0rd!"
DBconn = mdb.connect(host="localhost",user="root",passwd=pwd,db="temphumid_database")
cursor = DBconn.cursor()
# sql connect and specify channels
sql = "select datetime,temperature,humidity from temphumidLog"

df = pd.read_sql('SELECT * FROM temphumidLog',con=DBconn)
print df
#print df.dtypes
#print type(df)

#df.plot(x="datetime")
#plt.xticks(xValues)
#xfmt=mdates.DateFormatter('%d-%m-%y %H-%M')
#pylab.show()

##plt.grid(True)
#plt.ylabel('Temp C, RH %%')
#plt.axis(ymax=100,ymin=0)
#plt.xlabel(time.asctime())
#plt.title("<location_name> Temperature (Red), Humidity (Green)")
#plt.hold(True)

## and some fiddly bits around formatting the X (date) axis
#plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
#plt.gca().xaxis.set_major_locator(mdates.HourLocator())
##lines = plt.plot(x="datetime",df)
##plt.gcf().autofmt_xdate()

#pylab.show()

df.plot(x=df.datetime)
pylab.show()