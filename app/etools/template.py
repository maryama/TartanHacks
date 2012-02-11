"""Template and Rendering Tools"""

from genshi.template import TemplateLoader

from etools import Decorator


class Renderable(object):

    def __init__(self, content, template, type):
        self.content = content
        self.template = template
        self.type = type
        
    def __iter__(self): return self.content.__iter__()

class loader(Decorator):
    """Creates a template loader on the provided directory.
    
    Note that the directy is determined relative to the initial script
    (the '__main__' module), not the current module.
    """

    loader_cache = {}
    
    def __init__(self, directory = '.'):
        self.directory = directory
        if directory not in loader.loader_cache:
            loader.loader_cache[directory] = (
              TemplateLoader(directory, auto_reload = True))
        self.loader = loader.loader_cache[directory]

    def wrapper(self, *args, **kwargs):
        obj = self.wrapped(*args, **kwargs)
        if isinstance(obj, Renderable):
            tmpl_gen = self.loader.load(obj.template)
            return tmpl_gen.generate(**obj.content
                ).render(obj.type, doctype = obj.type)
        return obj
    
    
class returnrenderable(Decorator):
        
    def __init__(self, template, type = 'html'):
        self.template = template
        self.type = type
        
    def wrapper(self, *args, **kw):
        content = self.wrapped(*args, **kw)
        return Renderable(content, self.template, self.type)
        
class render(Decorator):

    loader_cache = {}

    def __init__(self, template, root = '.', type = 'html'):
        if root not in render.loader_cache:
            render.loader_cache[root] = (
              TemplateLoader(root, auto_reload = True))
        loader = render.loader_cache[root]
        self.tmpl_gen = loader.load(template)
        self.type = type
        
    def wrapper(self, *args, **kwargs):
        content = self.wrapped(*args, **kwargs)
        return self.tmpl_gen.generate(**content
          ).render(self.type, doctype = self.type)