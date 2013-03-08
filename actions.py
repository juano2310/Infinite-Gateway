#!/usr/bin/python
# coding=UTF-8

print "Starting Infinite Gateway Activity Monitor"

import sys,os
from igconfig import *

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
	try:
	    import MySQLdb
	except ImportError:
	    print "Error: You need to install MySQL extension for Python"
	    sys.exit(1)
	
	while True:
		try:
		    db = MySQLdb.connect (MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
		except:
			print "Error connecting to the Database"
			sys.exit (1)
	
		cursor = db.cursor ()
	
		cursor.execute ("SELECT * FROM actions_triggered where actions_triggered_executed = '0000-00-00 00:00:00'")
		rows = cursor.fetchall ()
			
		for row in rows:      
		   	actions_id = row[0]
		   	actions_type = 'py'
		   	actions_file = "%s%s%s%s%s%s" % ('python /var/infinitegateway/actions/',row[1],'/main.',actions_type,' ',row[2])	    		
		   	os.system(actions_file)
		   	cursor.execute ("UPDATE actions_triggered SET actions_triggered_executed=NOW() WHERE actions_triggered_id=%s",(actions_id))  
		   	db.commit() 
		cursor.close ()
		db.close ()