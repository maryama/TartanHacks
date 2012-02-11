import yql 
import json

def search_bkmrks(term, site_list):
  conn = yql.Public()
  env = "http://datatables.org/alltables.env"

  results = [] 
  for site in site_list:
    query = []
    query.append("select * from google.search where q=\"")
    query.append(term)
    query.append(' inurl:')
    query.append(site)
    query.append('\"')

    result = conn.execute(''.join(query), env=env)
    for row in result.rows:
      h_result = { 'title' : row.get('title'),
                   'content' : row.get('content'),
                   'url' : row.get('url')
                 }
      results.append(h_result)

    return results 

'''
http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20google.search%20where%20q%3D%22tartans%20inurl%3Acmu.edu%22&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=cbfunc
'''
