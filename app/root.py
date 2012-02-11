import cherrypy
from cherrypy import expose

from genshi.template import TemplateLoader
loader = TemplateLoader('app/view/templates', auto_reload=True)

class Root(object):

  @expose
  def index(*args, **dargs):
    tmpl = loader.load('index.html')
    page = tmpl.generate(title='Inspektor')
    return page.render('html', doctype='html')
    
'''
    # something for loading page with groups
    @expose
    def index2(*args, **dargs):
        tmpl = loader.load('index2.html')
        page = tmpl.generate(links=True)
        return page.render('html', doctype='html')
    
    # something for loading page with links
    @expose
    def index3(*args, **dargs):
        tmpl = loader.load('index3.html')
        page = tmpl.generate(links=True)
        return page.render('html', doctype='html')
'''
