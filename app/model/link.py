
from sqlalchemy.orm import mapper

from etools import Record

#from .
import DB

#TODO: fix records
class Link(Record):

    def __init__(self,
                 url = None,
                 title = None,
                 twitter_handle = None
                 ):

        Record.__init__(**locals)

    def __composite_values__(self):
        return [
            self.url,
            self.title,
            self.twitter_handle
            ]

    #CRUD Methods

    @staticmethod
    def select(username, session):
        return session.query(User).filter_by(username=username).one()

    def insert(self, session):
        with self.transaction(session):
            session.add(self)

    def update(self, session, **data):
        with self.transaction(session):
            Record.update_existing(self, **data)

    def delete(self, session):
        with session.begin():
            session.delete(self)
        del self
mapper(Link, DB.link_info)
