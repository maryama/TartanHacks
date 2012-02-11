import cherrypy
#import etools.web.cptools as etools

#from .root import Root
#from .model import db

#Create and configure app

class Root(object):
    
    @cherrypy.expose
    def index(*args, **dargs):
        return "Hello, World!"


application = cherrypy.Application(Root())

#Add toolboxes
#application.toolboxes['etools'] = etools

def configure(): pass
#    etools.configureDB(db, application)
