"""Validation ETools"""

import logging
from inspect import getargspec

import formencode
from formencode import variabledecode, htmlfill

from etools import Decorator


log = logging.getLogger(__name__)
            
class validate(Decorator):
    """Wrong
    
    Validate input either for a FormEncode schema, or individual
    validators

    Given a form schema or dict of validators, validate will attempt to
    validate the schema or validator list.

    If validation was successful, the valid result dict will be saved
    as ``self.form_result``. Otherwise, the action will be re-run as if
    it was a GET, and the output will be filled by FormEncode's
    htmlfill to fill in the form field errors.

    ``schema``
        Refers to a FormEncode Schema object to use during validation.
    ``form_page``
        Method used to display the form, which will be used to get the 
        HTML representation of the form for error filling.
    ``variable_decode``
        Boolean to indicate whether FormEncode's variable decode
        function should be run on the form input before validation.
    ``dict_char``
        Passed through to FormEncode. Toggles the form field naming 
        scheme used to determine what is used to represent a dict. This
        option is only applicable when used with variable_decode=True.
    ``list_char``
        Passed through to FormEncode. Toggles the form field naming
        scheme used to determine what is used to represent a list. This
        option is only applicable when used with variable_decode=True.
    ``state``
        Passed through to FormEncode for use in validators that utilize
        a state object.

    Example::

        class SomeController(BaseController):

            def create(self, id):
                return render('/myform.mako')

            @validate(schema=model.forms.myshema(), form='create')
            def update(self, id):
                # Do something with self.form_result
                pass

    """
    
    def __init__ (self, validators = None, form_page = None, 
            error_handler = None, variable_decode=False,
            dict_char='.', list_char='-', state=None,
            **htmlfill_kwargs):
        
        self.validators = validators
        
        self.validate = self.selectValidator()
        
        self.form_page = form_page
        self.error_handler = error_handler
        self.variable_decode = variable_decode
        self.dict_char = dict_char
        self.list_char = list_char
        self.state = state
        self.htmlfill_kwargs = htmlfill_kwargs
        
        
    def selectValidator(self):
        """The validator may be a dictionary, a FormEncode Schema object, or any
        object with a "validate" method."""
        
        if isinstance(self.validators, dict):
            return self.dictValidate
        if isinstance(self.validators, formencode.Schema):
            return self.schemaValidate
        if hasattr(self.validators, 'validate'):
            return self.objectValidate
        
        
    def dictValidate(self, decoded):
        """Developers can pass in a dict of param names and FormEncode
        validators.  They are applied one by one and builds up a new set
        of validated params."""
        
        log.debug("Validating against provided validators")

        #Initialize valid_args and errors for use in iteration over the validators
  
        valid_args = {}
        errors = {}
                
        for field, validator in self.validators.iteritems():
            try:
                # XXX: Is this necessary to call twice?
                #validator.to_python(params.get(field), state)
                valid_args[field] = validator.to_python(decoded.get(field),
                        self.state)
            # catch individual validation errors into the errors dictionary
            except formencode.Invalid, inv:
                errors[field] = inv
                
        # If there are errors, create a compound validation error based on
        # the errors dictionary, and raise it as an exception
        if errors:
            raise formencode.Invalid(
                formencode.schema.format_compound_error(errors),
                decoded , None, error_dict=errors)
    
        return valid_args
    
    def schemaValidate(self, decoded):
        """A FormEncode Schema object - to_python converts the incoming
        parameters to sanitized Python values"""
                
        log.debug("Validating against a schema")
                
        return self.validators.to_python(decoded, self.state)
    
    def objectValidate(self, decoded):
        """An object with a "validate" method - call it with the parameters."""
        
        log.debug("Validating against an object with 'validate' defined")
        
        return self.validators.validate(decoded, self.state)
    
    def decodeVar(self, kwargs):
        log.debug("Running variable_decode on params")
        decoded = variabledecode.variable_decode(kwargs, self.dict_char,
                                                     self.list_char)
        return decoded
        
        
    def wrapper(self, *args, **kwargs):
                
        if self.variable_decode:
            decoded = self.decodeVar(kwargs)
        else:
            decoded = kwargs
            
        try: 
        
            valid_args = self.validate(decoded)
                
            kwargs.update(valid_args)
            return self.wrapped(*args, **kwargs)
            
        except formencode.Invalid, e:
            errors = e.unpack_errors(self.variable_decode, self.dict_char, self.list_char)
        
            log.debug("Errors found in validation, parsing form with htmlfill "
                      "for errors")

            # If a specific error handler is specified, evaluate and return it
            if self.error_handler:
                return self.error_handler(*args, **kwargs)

            # If there's no form supplied, just continue with the current
            # function call.
            if not self.form_page:
                return self.wrapped(*args, **kwargs)

            if getargspec(self.form_page).keywords == None:
                form_content = self.form_page(*args)
            else:
                form_content = self.form_page(*args, **kwargs)

            form_content = htmlfill.render(form_content, defaults=kwargs,
                                           errors=errors, **self.htmlfill_kwargs)

            return form_content
