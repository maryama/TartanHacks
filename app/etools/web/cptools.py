"""Cherrypy related tools"""

from sys import exc_info

import cherrypy
from cherrypy import expose, request
from cherrypy._cptools import HandlerWrapperTool, Tool, Toolbox
from cherrypy._cpdispatch import LateParamPageHandler

from etools import arg2kw, try_update_wrapper
from sqlalchemy.orm import scoped_session

tools = Toolbox('etools')


class HandlerDecoratorTool(HandlerWrapperTool):
    """Like HandlerWrapperTool, but uses a Decorator class
    as its callable and supports configuration as a normal tool does.
    
    Note that the given Decorator class must define an __init__ method, and 
    thus must require a function call when used by itself, even with 
    no arguments. This is for consistency with the usage of a Tool as 
    a decorator, which also requires a call in the decorator.
    """
     
    def __init__(self, decoratorcls, point='before_handler', name=None, priority=50):
        self.decoratorcls = decoratorcls
        self._point = point
        self._name = name
        self._priority = priority
        
        try_update_wrapper(self.callable.__func__ , self.decoratorcls)
        try_update_wrapper(self, self.decoratorcls)
    
    def callable(self, *args, **kwargs):
        handler = cherrypy.serving.request.handler
        
        if isinstance(handler, cherrypy.NotFound): return
        
        innermeth = handler.callable
        
        innerfunc = innermeth.__func__
        owner = innermeth.__self__
        
        wrapper = self.decoratorcls(*args, **kwargs)(innerfunc)
        wrapper = wrapper.__get__(owner)
        
        try_update_wrapper(wrapper, innermeth)
        
        hargs = handler.args
        hkwargs = handler.kwargs
        
        newhandler = LateParamPageHandler(wrapper, *hargs, **hkwargs)
        
        cherrypy.serving.request.handler = newhandler
       
    def __call__(self, *args, **kwargs):
        if '__init__' in self.decoratorcls.__dict__:
            kwargs.update(arg2kw(args, self.decoratorcls.__init__, bind = True))
            #return super(self.__class__, self).__call__(**kwargs)
            return Tool.__call__(self, **kwargs)
        else:
            #return super(self.__class__, self).__call__()
            return Tool.__call__(self, **kwargs)

            
    
def staticpage(page):
    
    @expose
    def page_func(self):
       with open(page) as page_file:
           html = page_file.read()
       return html
        
    return page_func
    
    
import types 

class ExposedCls(type):
   def __init__(cls, name, bases, dict):
      super(ExposedCls, cls).__init__(name, bases, dict)
      for name, value in dict.iteritems():
        if callable(value) and not name.startswith('_'):
           value.exposed = True

class Controller(object):
    __metaclass__ = ExposedCls


def configureDB(db, app):
    db.configure(**app.config['Database'])
            
            
 
from etools.template import render
tools.template = HandlerDecoratorTool(render, priority = 10)

from etools.web.validation import validate
tools.validate = HandlerDecoratorTool(validate)



globals().update(tools.__dict__)
tools.__dict__.update(globals())
