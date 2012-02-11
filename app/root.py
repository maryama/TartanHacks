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
  def index(self, *args, **dargs):
    tmpl = loader.load('index.html')
    page = tmpl.generate()
    return page.render('html', doctype='html')
    
  @expose
  def login(self, *args, **dargs):
    config = cherrypy.request.app.config
    raise cherrypy.HTTPRedirect("https://www.facebook.com/dialog/oauth?"
     + "client_id={appid}&redirect_uri={url}".format(
        **config['Facebook']))

  @expose
  def bookmarks(self,
                code = None,
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
      return external.read()
      token_query = external.read()
      external.close()
      try:
        query_site = urlopen(
          'https://graph.facebook.com/me?' + token)
        query = json.loads(query_site.read())
        id = query['id']
        return number

      except ValueError:
        return token_query
      except IndexError:
        return "Failed"
      finally:
        query_site.close()

    # something for loading page with groups
    @expose
    def groups(self, *args, **dargs):
        tmpl = loader.load('index2.html')
        page = tmpl.generate(links=True)
        return page.render('html', doctype='html')
    
    # something for loading search results
    @expose
    def search(self, *args, **dargs):
        tmpl = loader.load('index2.html')
        page = tmpl.generate(links=True)
        return page.render('html', doctype='html')
    
    # something for loading page with links
    @expose
    def index3(self, *args, **dargs):
        tmpl = loader.load('index3.html')
        page = tmpl.generate(links=True)
        return page.render('html', doctype='html')
