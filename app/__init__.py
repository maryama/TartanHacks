import cherrypy
#import etools.web.cptools as etools

from .root import Root
#from .model import db

#Create and configure app

application = cherrypy.Application(Root())

#Add toolboxes
#application.toolboxes['etools'] = etools

def configure(): pass
#    etools.configureDB(db, application)
