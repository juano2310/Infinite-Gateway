#!/usr/bin/python
# coding=UTF-8

print "Starting Infinite Gateway Conditions Monitor"

import sys,os,datetime,time
from igconfig import *
from datetime import date

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
	
		#Locks the sensor data that is going to be processed
		cursor.execute ("UPDATE devices_log SET devices_log_processing='1' WHERE devices_log_processing='0'")  
		db.commit() 
		
		#Checks if the objective is active (makes sure that the objective is active and on during this day and time)
		cursor.execute ("SELECT * FROM objectives WHERE objectives_steps<>0 and objectives_active=1")
		objectives = cursor.fetchall ()

		today = date.today().weekday() + 6
		timenow = strftime("%H:%M:%S", gmtime())
		
		#For each active objective check the condition for the current step
		for row in objectives:
			objectives_day = row[today]
			objectives_timenow = time.strptime(timenow,"%H:%M:%S")
			objectives_time0 = time.strptime("00:00:00","%H:%M:%S")
			objectives_time1 = time.strptime(str(row[13]),"%H:%M:%S")      
			objectives_time2 = time.strptime(str(row[14]),"%H:%M:%S") 
		   	objectives_active = 0
		   	# !!! Date, Time (makes sure that the objective is active and on during this day and time)
		   	if objectives_day == 1:
				if (((objectives_time1 == objectives_time0 or objectives_time1 == objectives_timenow) and objectives_time2 == objectives_time0) or ((objectives_time1 <= objectives_timenow and objectives_timenow <= objectives_time2) and objectives_time1 <> objectives_time0)):
		   			objectives_active = 1
		   			   	
		   	if objectives_active == 1:
			   	objectives_id = row[0]
			   	objectives_step = row[3]
			   	objectives_updated = row[5] 
			   	objectives_next_step = objectives_step + 1
			   	conditions_final = 1 #Assume conditions are true
			   		   		   	
			   	#Check if all the conditions in the objective / step are true
				cursor.execute ("SELECT * FROM conditions WHERE objectives_id=%s and objectives_step=%s and conditions_status=1 ORDER BY conditions_type DESC", (objectives_id,objectives_next_step))
				conditions = cursor.fetchall ()
				for condition in conditions:
					if conditions_final != 0:
						condition_value = condition[7]			
		
						# !!! Check the condition time
						if condition[1] == 'T':	
							cursor.execute ("SELECT  NOW()")
							dbtime = cursor.fetchone()
							dbdiff = (time.mktime(dbtime[0].timetuple()) - time.time()) #Ajusts the difference with a DB in a different timezone
							lastupdate = time.time() - time.mktime(objectives_updated.timetuple()) + dbdiff
							if lastupdate < condition_value:
									conditions_final = 0	
										
						# !!! Check the condition device
						if condition[1] == 'D':			
							cursor.execute ("SELECT * FROM devices_log WHERE devices_log_processing=1 AND devices_log_processed=0 AND devices_log_address=%s",(condition[4]))	
							devicelog = cursor.fetchall ()
							ioposition = condition[5]+3
							condition_operator = condition[6]
							condition_aux = 0 #Assume condition is false	
													
							for info in devicelog:
								if condition_operator == "=":
									if condition_value == info[ioposition]:
										condition_aux = 1
								if condition_operator == ">":
									if condition_value > info[ioposition]:
										condition_aux = 1
								if condition_operator == "<":
									if condition_value < info[ioposition]:
										condition_aux = 1																								
								if condition_operator == ">=":
									if condition_value >= info[ioposition]:
										condition_aux = 1
								if condition_operator == "<=":
									if condition_value <= info[ioposition]:
										condition_aux = 1	
								if condition_operator == "!=":
									if condition_value != info[ioposition]:
										condition_aux = 1
										
							if condition_aux == 0: 	
								conditions_final = 0					
						
						# !!! Check the condition web service
		#				if condition[1] == 'W': 
		#					condition_status = condition[value] condition[operator] objectives_updated							
				
						
				if conditions_final == 1: #If all conditions are true move to next step						
					cursor.execute ("UPDATE objectives SET objectives_updated=NOW(), objectives_step=%s WHERE objectives_id=%s",(objectives_next_step,objectives_id))  
					db.commit() 			
	
		#For each completed objective add the actions to actions_triggered
		cursor.execute ("SELECT * FROM objectives WHERE objectives_step>=objectives_steps and objectives_steps<>0")
		objectives = cursor.fetchall ()
		
		for row in objectives:    
		   	objectives_id = row[0]	   	
			cursor.execute ("SELECT * FROM objectives_actions WHERE objectives_id=%s", (objectives_id))
			actions = cursor.fetchall ()	   	
		   	
			for action in actions:   	   	
			   	action_file = action[3]
			   	action_params = action[4]
				cursor.execute ("""INSERT INTO actions_triggered (actions_file,actions_options) VALUES (%s,%s)""",(action_file,action_params))	
				db.commit()		
			
			cursor.execute ("UPDATE objectives SET objectives_step=0, objectives_updated=NOW() WHERE objectives_id=%s",(objectives_id)) 			
			db.commit()		   	
	
		#Set the sensor information as processed
		cursor.execute ("UPDATE devices_log SET devices_log_processed=NOW() WHERE devices_log_processing='1' AND devices_log_processed=0")  
		db.commit() 
	
		cursor.close ()
		db.close ()