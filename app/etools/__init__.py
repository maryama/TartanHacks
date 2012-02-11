
from functools import update_wrapper
from inspect import getargspec
from copy import copy

def try_update_wrapper(*args, **kw):            
    """In most cases, this will update the wrapper's attributes with those 
    of the wrapped function. However, if func is some object that doesn't 
    have the normal function attributes, the attribute error is ignored.
    """
    
    try:
        update_wrapper(*args, **kw)
    except AttributeError: pass


class block(object):

    def __call__(self, blok):
        if self.param == '':
            return self.func(blok, *self.args, **self.kw)
        else:
            kw = self.kw + {self.param: blok}
            return self.func(*self.args, **kw)

    def __init__(self, func = lambda x: x, param = '', *args, **kw):
        self.func = func
        self.param = param
        self.args = args
        self.kw = kw

class Decorator(object):
    
    def __new__(cls, *args, **kw):
        self = object.__new__(cls)
        if '__init__' in cls.__dict__:
            return self
        return self.__call__(*args, **kw)
    
    def __call__(self, wrapped):
        self.wrapped = wrapped
        
        # Due to various limitations on methods, such as restricted attributes,
        # the decorator must return an unbound function, not a method.
        # Therefore, this function encapsulates the wrapper method 
        # and is returned.
        def closure(*args, **kw):
            return self.wrapper(*args, **kw)
            
        try_update_wrapper(closure, wrapped)
        
        return closure
    
    def wrapper(self, *args, **kw):
        return self.wrapped(*args, **kw)
        
        
def arg2kw (args, func, bind = False):
    kw = {}
    params = getargspec(func).args
    if bind == True:
        params = params[1:]
    for param, arg in zip(params, args):
        kw[param] = arg
    return kw


class lazyattr(object):

    def __init__(self, eval_):
        self.eval_ = eval_
        
    def __get__(self, obj, objtype = None):
        if obj is None:
            return self
        value = self.eval_(obj)
        setattr(obj, self.eval_.__name__ , value)
        return value
        

def import_for_modules(module_str, call_globals, call_locals):
    """Function for only importing if an existing module is imported
    
    Given a format string specifying the name of the module to import
    using 'module' as the substite variable, returns a function that
    given the name of a module to look for, if found, will substitute 
    that name with 'module' in str and import the module in the 
    current package with that name
    """
    
    def import_from_if_using(module):
    
        import sys
    
        if module in sys.modules:
            addedmodule = __import__(module_str.format(module = module), 
                                      call_globals, call_locals, [] , 1)
            call_globals.update(addedmodule.__dict__)
            
    return import_from_if_using


class semistaticmethod(staticmethod):

    def __get__(self, instance, owner):
        if instance is None:
            return staticmethod.__get__(self, instance, owner)
        else:
            return staticmethod.__get__(self, instance, owner).__get__(instance, owner)

class Record(dict):

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

    @semistaticmethod
    def update(self, *args, **kwargs):
        dict.update(self.__dict__, *args, **kwargs)

    @semistaticmethod
    def update_existing(self, *args, **kwargs):
        final_kwargs = kwargs.copy()
        for i in kwargs:
            if i not in self.__dict__: del final_kwargs[i]
        Record.update(self, *args, **final_kwargs)
        
            
