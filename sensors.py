#!/usr/bin/python
# coding=UTF-8

print "Starting Infinite Gateway Sensors Monitor"

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

with daemon.DaemonContext():

	# Open serial port
	ser = serial.Serial(XBEE_PORT, XBEE_BAUD_RATE)
	
	# Create API object
	xbee = ZigBee(ser)
	
	# Continuously read packets and store data
	while True:
		response = xbee.wait_read_frame() 
		sensor_long_address = response['source_addr_long'].encode('hex_codec') 
		sensor_short_address = response['source_addr'].encode('hex_codec') 
		sensor_id = response['id']
		
		if sensor_id == "rx":
		    sensor_data = response['rf_data']       
		else:
			sensor_data = response['samples']        
		
		try:
		    db = MySQLdb.connect (MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
		except:
			print "Error connecting to the Database"
			sys.exit (1)
			
		cursor = db.cursor ()
		
		# Check if the device exist. If not is creates it and is set as pending.
		cursor.execute ("SELECT * FROM devices where devices_long_address=%s",(sensor_long_address))
		rows = cursor.fetchall ()
		if not rows:
			try:
				cursor.execute ("""INSERT INTO devices (devices_long_address,devices_short_address) VALUES (%s,%s)""", (sensor_long_address,sensor_short_address))
				db.commit()
			except:
				db.rollback()
		else:			
			# Check if it is authorize to operate
			for row in rows:
				if row[10] == 'E':
					# Update with last Short Address
					cursor.execute ("UPDATE devices SET devices_short_address=%s WHERE devices_long_address=%s", (sensor_short_address,sensor_long_address))        
					db.commit()     							    
					if sensor_id == "rx":
						cursor.execute ("""INSERT INTO devices_log (devices_log_address,devices_log_rx) VALUES (%s,%s)""", (sensor_long_address,sensor_data))    
						db.commit()  
					else:
						# Insert data in the DB
						data_io0 = 0
						data_io1 = 0
						data_io2 = 0   						   						
						data_io3 = 0
						data_io4 = 0 
						for data in sensor_data[0]:
							data_aux = data[-1]  					
							if data_aux == '0':
								data_io0 = sensor_data[0][data] 								
							if data_aux == '1':
								data_io1 = sensor_data[0][data] 								
							if data_aux == '2':
								data_io2 = sensor_data[0][data] 								
							if data_aux == '3':
								data_io3 = sensor_data[0][data]
							if data_aux == '4':
								data_io4 = sensor_data[0][data]									
						cursor.execute ("""INSERT INTO devices_log (devices_log_address,devices_log_io0,devices_log_io1,devices_log_io2,devices_log_io3,devices_log_io4) VALUES (%s,%s,%s,%s,%s,%s)""", (sensor_long_address,data_io0,data_io1,data_io2,data_io3,data_io4))    	           
						db.commit() 
		cursor.close () 
		db.close ()		

