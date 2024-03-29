"""Interface for SQLALchemy"""

from contextlib import contextmanager

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

from .dburl import dburl
from . import _interface as base

interface = 'SQLAlchemy'

class DBInterface(base.DBInterface): 

    def __init__(self, metadata, **engine_args):
        
        self.config = None
        self.dburl = None
        self.engine = None
        
        self.metadata = metadata
        self.engine_args = engine_args

    def configure(self, **config):
        self.config = config
        self.dburl = dburl(**self.config)
        self.engine = create_engine(self.dburl, **self.engine_args)
        self.metadata.bind = self.engine
        self.metadata.create_all()


class TransactionMaker(base.TransactionMaker):

    def __init__(self, SessionCls):
        self.SessionCls = SessionCls
        
    def __enter__(self):
        self.session = self.SessionCls()
        return self.session
        
    def __exit__(self, type, value, msg):
    
        # deconfigure (unbind) session so it is ready for next request
        self.session.close()
        
        #If there's an error, it should not be suppressed
        return False

        
@contextmanager
def instance_transaction(obj, session):
    with session.begin():
        yield session
    session.refresh(obj)
    
    
def configureSQLAlchemy(
      
      #Engine Parameters
      dialect, driver = '', username = '', 
      password = '', host = '', port = '', database = '', URLArgs = '', 
     
      #Session Parameters
      scoped = False, autocommit = False, autoflush = True,
      _enable_transaction_accounting = True, expire_on_commit = True, 
      twophase = False, weak_identity_map = True, 
      #Non-Boolean Arguments
      class_ = None, extension = None, query_cls = None,
     
      #Keyword Parameters for the engine
      **enginekwargs):
    
    global metadata, Session, engine
    
    
    #Create engine
    
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
    
    connURL = dialectStr + '://' + userStr + hostStr + DBStr + URLArgs
    
    engine = create_engine(connURL, **enginekwargs)
    
    
    #Create metadata
    metadata = MetaData()
    
    
    #Create Session
    
    sessionargs = dict(
      autocommit = autocommit,
      autoflush = autoflush,
      _enable_transaction_accounting = _enable_transaction_accounting,
      expire_on_commit = expire_on_commit, 
      twophase = twophase, 
      weak_identity_map = weak_identity_map,
      class_ = class_,
      extension = extension, 
      query_cls = query_cls
    )
    
    if not class_:
        del sessionargs['class_']
    if not extension:
        del sessionargs['extension']
    if not query_cls:
        del sessionargs['query_cls']
        
    Session = sessionmaker(bind = engine, **sessionargs)
    if scoped:
        Session = scoped_session(Session)
        
    class DB(object): pass
        
    db = DB()
    db.metadata = metadata
    db.Session = Session
    db.engine = engine
    return db
