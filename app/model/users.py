"""The different kinds of users in the system"""

from sqlalchemy.orm import mapper, relationship

from etools import Record
from etools.data.db import instance_transaction

#from .
import DB, contact

class User(object):
    
    def __init__(self, username, password, contact = None): Record.update(**locals())

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
       polymorphic_on = DB.user_accounts.c.group, polymorphic_identity = 'user',
       properties = { 'contact': relationship(contact.Contact) }
       )
    
class Moderator(User): pass

class Employer(User):

    def __init__(self,
                 **user):

        User.__init__(self, **user)
        del user
        
        Record.update(**locals)

class Student(User):

    def __init__(self, lname, fnmame, mname,
                 qualifications, pos_hours,
                 **user):

        User.__init__(self, **user)
        del user

        Record.update(**locals)
