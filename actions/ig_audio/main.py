#!/usr/bin/env python
#
# Action: Play Sound
# Ver: 1.0
# Author: Juano
# Author URL: infinitegateway.org
# Options: MP3 file

import os,sys

options = sys.argv[1:]

if not options:
	print 'The file name is empty'
else:
	audiofile= '%s%s' % ('mpg321 /var/www/sound/', options[0])
	os.system(audiofile)

       