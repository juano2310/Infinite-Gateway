#!/usr/bin/env python
#
# Action: Send text
# Ver: 1.0
# Author: Juano
# Author URL: infinitegateway.org
# Options: Number, Subject, Message, Gmail User, Gmail password

import os,sys
import getopt
import subprocess
import smtplib
import socket
from email.mime.text import MIMEText

options = sys.argv[1:]

if not options:
	print 'Sending information is required'
else:
	to = '%s%s' % (options[0],'@vzwpix.com')

	try:
		subject = options[1]
	except IndexError:
		subject = 'Infinite Gateway' 	
	try:
		message = options[2]
	except IndexError:
		message = 'This message was delivered because the system failed to identify a valid Message' 
			
	gmail_user = 'alert@infinitegateway.org'
	gmail_password = '23Ig%1729'
	smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(gmail_user, gmail_password)
	
	msg = MIMEText(message)
	msg['Subject'] = subject
	msg['From'] = gmail_user
	msg['To'] = to
	smtpserver.sendmail(gmail_user, [to], msg.as_string())
	smtpserver.quit()