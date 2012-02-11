import cherrypy

from cherrypy import expose


class Root(object):

    @expose
    def index(*args, **dargs):
        return "Hello, World"
