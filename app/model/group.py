
from sqlalchemy.orm import mapper

from etools import Record

#from .
import DB

class Group(Record):

    def __init__(self,
                 name = None,
                 num_links = 0,
                 time_accessed = None
                 ):

        Record.__init__(**locals)
        self.links = None

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
    def select(group_id, session):
        return session.query(Group).filter_by(group_id=group_id).one()

    def insert(self, session):
        with self.transaction(session):
            session.add(self)

    def update(self, session, **data):
        with self.transaction(session):
            Record.update_existing(self, **data)

    def get_links(self, session, links_table):
        with self.transaction(session):
            self.groups = session.query(links_table).filter_by(group_id=self.group_id)

    def delete(self, session):
        with session.begin():
            session.delete(self)
        del self

mapper(Group, DB.group_info)
