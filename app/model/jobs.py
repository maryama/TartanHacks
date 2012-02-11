

from sqlalchemy.orm import mapper, relationship

from etools import Record
from etools.data.db import instance_transaction

#from .
import DB

class Job(object):

    def __init__(self,
                 title, description, qualifications, hours,
                 days, pay, duties):

        Record.update(**locals)

    transaction = instance_transaction

    #CRUD Methods

    @staticmethod
    def select(id, session):
        return session.query(Job).filter_by(id=id).one()

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

mapper(Job, DB.jobs)
