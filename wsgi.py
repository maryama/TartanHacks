#!/usr/bin/env python

import sys
import os

import cherrypy
from paste import evalexception
from paste.httpexceptions import *


import site

# Site-wide (global) config
cherrypy.config.update({'environment': 'staging',
                        'log.error_file': 'site.log',
                        'request.throw_errors': True,
                        'log.screen': True,
                        'engine.autoreload_on': True,
                        'tools.staticdir.root': os.path.abspath('.')
                        })


#Assign the app to application

application = site.app 

     
#Add development-exclusive app configuration
application.wsgiapp.pipeline.append(('paste_exc', evalexception.middleware.EvalException))                  
                 
# Mount each app and pass it its own config
cherrypy.tree.mount(application, "/", 'crnjobs_dev.ini')

#Configure each app
site.configure()

if __name__ == '__main__':
    
    #Start the engine
    cherrypy.engine.start()
    cherrypy.engine.block()
    cherrypy.engine.stop()
