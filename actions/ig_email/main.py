#!/usr/bin/env python
#
# Action: Send email
# Ver: 1.0
# Author: Juano
# Author URL: infinitegateway.org
# Options: Email, Subject, Message, Gmail User, Gmail password

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
	to = options[0]

	try:
		subject = options[1]
	except IndexError:
		subject = 'Infinite Gateway' # 'Washing Machine'	
	try:
		message = options[2]
	except IndexError:
		message = 'Testing Message' # 'The washing cycle has been completed. You can now proceed to remove items from the washer.'		
	
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