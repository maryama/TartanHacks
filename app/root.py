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
    page = tmpl.generate()
    return page.render('html', doctype='html')
    
  @expose
  def login(*args, **dargs):
    config = cherrypy.request.app.config
    raise cherrypy.HTTPRedirect("https://www.facebook.com/dialog/oauth?"
     + "client_id={appid}&redirect_uri={url}".format(
        **config['Facebook']))

  @expose
  def bookmarks(code = None,
             error_reason = None,
             error = None,
             error_description = None):
    config = cherrypy.request.app.config
    if error: return "Login Failure."
    if code:
      external = urlopen(
        "https://graph.facebook.com/oauth/access_token?" +
        "client_id={appid}".format(**config['Facebook']) +
        "&redirect_uri={url}".format(**config['Facebook']) +
        "&client_secret={secret}&".format(**config['Facebook']) +
        "&code=" + code)
      token_query = json.loads(external.read())
      external.close()
      try:
        token = token_query['access_token']
        query_site = urlopen(
          'https://graph.facebook.com/me?access_token={token}'.format(
            token = token))
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
