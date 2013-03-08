#!/usr/bin/python2.4

import getopt, os, sys, twitter

sys.path.append('../')

from igconfig import *
   
options = sys.argv[1:]

try:
	message = options[0]
except IndexError:
	print 'Error: The system failed to identify a valid message' 
	sys.exit(1)

try:
	user = options[1]
except IndexError:
	print 'Error: The system failed to identify a valid user' 
	sys.exit(1)

try:
    import MySQLdb
except ImportError:
    print "Error: You need to install MySQL extension for Python"
    print "sudo apt-get install python-mysqldb"
    sys.exit(1)

try:
    db = MySQLdb.connect (MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
except:
	print "Error connecting to the Database"
	sys.exit (1)

cursor = db.cursor ()
cursor.execute ("SELECT * FROM personal_twitter where personal_id=%s",(user))
row = cursor.fetchone ()
if row:
	consumer_key = row[1]
	consumer_secret = row[2]
	access_token_key = row[3]
	access_token_secret = row[4]
	
	api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token_key, access_token_secret=access_token_secret, debugHTTP=True)
	
	try:
		status = api.PostUpdate(message)
	except UnicodeDecodeError:
		print "Your message could not be encoded.  Perhaps it contains non-ASCII characters? "
		print "Try explicitly specifying the encoding with the --encoding flag"
		sys.exit(2)
		
	print "%s just posted: %s" % (status.user.name, status.text)

