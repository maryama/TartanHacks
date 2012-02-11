"""The different kinds of users in the system"""

from sqlalchemy.orm import mapper, relationship

from etools import Record
from etools.data.db import instance_transaction
#TODO: how do I get the groups here?

#from .
import DB

class User(object):
    
    def __init__(self,
                user_id = None): Record.update(**locals()):
      self.user_id = user_id
      self.groups = #how do i get the database stuff needed for this?

    def __composite_values__(self):
        return [ self.user_id ]

    #wut
    def __repr__(self):
        return '<{type} {username}>'.format(type = type(self), **self.__dict__)

    transaction = instance_transaction

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

mapper(User, DB.user_accounts,
       polymorphic_on = DB.user_accounts.c.group, polymorphic_identity = 'user')
