import json

from urllib2 import urlopen

import cherrypy
from cherrypy import expose

import sqlalchemy

from model import user 
from model import link 
from model import group 

from genshi.template import TemplateLoader
loader = TemplateLoader('app/view/templates', auto_reload=True)

class Root(object):

  @expose
  def index(*args, **dargs):
    tmpl = loader.load('index.html')
    page = tmpl.generate(title='Inspektor')
    return page.render('html', doctype='html')
    
  '''
  @expose
  def login():
    raise cherrypy.HTTPRedirect("https://www.facebook.com/dialog/oauth?
     client_id=YOUR_APP_ID&redirect_uri=YOUR_URL")
     '''

  @expose
  def logged(code = None,
             error_reason = None,
             error = None,
             error_description = None):
    if error: return "Login Failure."
    if code:
      external = urlopen(
        "https://graph.facebook.com/oauth/access_token?" +
        "client_id=YOUR_APP_ID"&
        "redirect_uri=YOUR_URL"
        "&client_secret=YOUR_APP_SECRET&"
        "code=" + code)
      token_query = json.loads(external.read())
      external.close()
      try:
        token = token_query['access_token']
        query_site = urlopen(
          'https://graph.facebook.com/me?access_token=ACCESS_TOKEN')
        query = json.loads(query_site.read())
        query_site.close()
        id = query['id']
        return number
        
      except IndexError:
        return "Failed"

    # something for loading page with groups
    @expose
    def groups(*args, **dargs):
        tmpl = loader.load('index2.html')
        page = tmpl.generate(links=True)
        return page.render('html', doctype='html')
    
    # something for loading search results
    @expose
    def search(*args, **dargs):
        tmpl = loader.load('index2.html')
        page = tmpl.generate(links=True)
        return page.render('html', doctype='html')
    
    # something for loading page with links
    @expose
    def index3(*args, **dargs):
        tmpl = loader.load('index3.html')
        page = tmpl.generate(links=True)
        return page.render('html', doctype='html')
