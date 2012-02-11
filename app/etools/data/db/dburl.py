

def dburl(dialect, driver = '', username = '', 
      password = '', host = '', port = '', database = '', 
      **kwargs):
      
    urlargs = ['?{key}={value}'.format(key=key, value=value) 
                for (key, value) in kwargs.items()]
                
    urlqstr = '&'.join(urlargs)
    
    
    dialectStr = dialect + (('+' + driver) if driver else '')
        
    if username:
        userStr = username + ((':' + password) if password else '')
    else:
        userStr = ''
    
    if host:
        hostStr = host + ((':' + port ) if port else '')
    else:
        hostStr = ''
    
    DBStr = ('/' + database) if database else ''
    
    connURL = dialectStr + '://' + userStr + hostStr + DBStr + urlqstr
    
    return connURL
