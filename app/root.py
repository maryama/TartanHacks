import cherrypy
from cherrypy import expose

from genshi.template import TemplateLoader
loader = TemplateLoader('app/view/templates', auto_reload=True)


class Root(object):

    @expose
    def index(*args, **dargs):
        tmpl = loader.load('index.html')
        page = tmpl.generate(link=None)
        return page.render('html', doctype='html')
        return 'Test'
