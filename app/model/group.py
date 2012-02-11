
from sqlalchemy.orm import mapper

from etools import Record

#TODO: how do I get the links here?
#from .
import DB

class Group(Record):

    def __init__(self,
                 name = None,
                 num_links = 0,
                 time_accessed = None
                 ):

        Record.__init__(**locals)

    def __composite_values__(self):
        return [
            self.name,
            self.num_links,
            self.time_accessed
            ]
        
    def update(self, **data):
        Record.update_existing(self, **data)

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
mapper(Group, DB.group_info)
