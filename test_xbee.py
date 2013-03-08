#!/usr/bin/python
# coding=UTF-8

print "Testing Infinite Gateway"
print

import sys,os
from igconfig import *

try:
	from xbee import XBee,ZigBee
except ImportError:
    print "Error: You need to install xbee extension for Python"
    print "sudo wget http://python-xbee.googlecode.com/files/XBee-2.0.0.tar.gz"
    print "sudo tar zxvf XBee-2.0.0.tar.gz"
    print "cd XBee-2.0.0"
    print "sudo python setup.py install"
    sys.exit(1)
try:
    import serial
except ImportError:
    print "Error: You need to install pyserial extension for Python"
    print "sudo apt-get install python-serial"
    sys.exit(1)
try:
    import MySQLdb
except ImportError:
    print "Error: You need to install MySQL extension for Python"
    print "sudo apt-get install python-mysqldb"
    sys.exit(1)

try:
	import daemon
except ImportError:
    print "Error: You need to install python-daemon extension for Python"
    print "$ sudo wget http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11-py2.7.egg#md5=fe1f997bc722265116870bc7919059ea"
    print "sudo sh setuptools-0.6c11-py2.7.egg"
    print "rm setuptools-0.6c11-py2.7.egg"
    print "sudo wget http://pypi.python.org/packages/source/p/python-daemon/python-daemon-1.5.5.tar.gz"
    print "sudo tar zxvf python-daemon-1.5.5.tar.gz$ cd python-daemon-1.5.5"
    print "sudo python setup.py install"
    sys.exit(1)

# Open serial port
ser = serial.Serial(XBEE_PORT, XBEE_BAUD_RATE)

# Create API object
xbee = ZigBee(ser)

formatter = "%s %s"

# Continuously read packets and print data
while True:
	response = xbee.wait_read_frame() 
	sensor_long_address = response['source_addr_long'].encode('hex_codec') 
	sensor_short_address = response['source_addr'].encode('hex_codec') 
	sensor_id = response['id']
	
	if sensor_id == "rx":
	    sensor_data = response['rf_data']       
	else:
		sensor_data = response['samples']        

	print "*********************************"	
	print formatter % ("Device Address: ", sensor_long_address)
	print formatter % ("Data: ", sensor_data)
	print "*********************************"