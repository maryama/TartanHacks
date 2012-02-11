"""The different kinds of users in the system"""

from sqlalchemy.orm import mapper, relationship

from etools.data.db import instance_transaction

#from .
import DB

class User(object):
    
    def __init__(self,
                user_id = None):
      self.user_id = user_id
      self.groups = None

    def __composite_values__(self):
        return [ self.user_id ]

    #wut
    def __repr__(self):
        return '<{type} {username}>'.format(type = type(self), **self.__dict__)

    transaction = instance_transaction

    #CRUD Methods

    @staticmethod
    def select(user_id, session):
        return session.query(User).filter_by(user_id=user_id).one()

    def insert(self, session):
        with self.transaction(session):
            session.add(self)

    def update(self, session, **data):
        with self.transaction(session):
            Record.update_existing(self, **data)

    def get_groups(self, session, groups_table):
        with self.transaction(session):
            self.groups = session.query(groups_table).filter_by(user_id=self.user_id)


    def delete(self, session):
        with session.begin():
            session.delete(self)
        del self

mapper(User, DB.groups)
