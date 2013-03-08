#!/usr/bin/python
# coding=UTF-8

print "Starting Infinite Gateway Halt Monitor"

from time import sleep
import os

try:
	import RPi.GPIO as GPIO
except ImportError:
    print "Error: You need to install RPi.GPIO for Python"
    print "sudo apt-get install python-dev"
    print "sudo apt-get install python-rpi.gpio"
        
try:
	import daemon
except ImportError:
    print "Error: You need to install python-daemon extension for Python"
    print "sudo wget http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11-py2.7.egg#md5=fe1f997bc722265116870bc7919059ea"
    print "sudo sh setuptools-0.6c11-py2.7.egg"
    print "rm setuptools-0.6c11-py2.7.egg"
    print "sudo wget http://pypi.python.org/packages/source/p/python-daemon/python-daemon-1.5.5.tar.gz"
    print "sudo tar zxvf python-daemon-1.5.5.tar.gz$ cd python-daemon-1.5.5"
    print "sudo python setup.py install"
    sys.exit(1)

with daemon.DaemonContext():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(23, GPIO.IN)
	 
	while True:
		if ( GPIO.input(23) == True ):
			os.system('sudo halt')

