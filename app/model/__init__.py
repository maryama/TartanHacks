

from sqlalchemy.orm import sessionmaker, scoped_session
from etools.data.db import DBInterface, TransactionMaker

#from .DB
from DB import metadata

db = DBInterface(metadata)

transaction = TransactionMaker(scoped_session(
        sessionmaker(autoflush = False, autocommit = True )))

