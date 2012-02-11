#!/usr/bin/env python

import sys
import os

import cherrypy


import app
from app import application

# Site-wide (global) config
cherrypy.config.update({
        'log.error_file': 'site.log',
        'tools.staticdir.root': os.path.abspath('.')})
      
                 
# Add config
application.merge('app_dev.ini')

#Configure each app
app.configure()
