#!/usr/bin/env python

import sys
import os

import cherrypy
from paste import evalexception
from paste.httpexceptions import *


import app
from app import application

# Site-wide (global) config
cherrypy.config.update({'environment': 'staging',
                        'log.error_file': 'site.log',
                        'request.throw_errors': True,
                        'log.screen': True,
                        'engine.autoreload_on': True,
                        'tools.staticdir.root': os.path.abspath('.')
                        })

     
#Add development-exclusive app configuration
application.wsgiapp.pipeline.append(('paste_exc', evalexception.middleware.EvalException))                  
                 
# Mount each app and pass it its own config
cherrypy.tree.mount(application, "/", 'app_dev.ini')

#Configure each app
app.configure()

if __name__ == '__main__':
    
    #Start the engine
    cherrypy.engine.start()
    cherrypy.engine.block()
    cherrypy.engine.stop()
