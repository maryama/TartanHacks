
from sqlalchemy.orm import mapper

from etools import Record

#from .
import DB

class Contact(Record):

    def __init__(self,
                 home_phone = None,
                 cell_phone = None,
                 email = None,
                 address= None
                 ):

        Record.__init__(**locals)

    def __composite_values__(self):
        return [
            self.home_phone,
            self.cell_phone,
            self.email,
            self.address
            ]
        
    def update(self, **data):
        Record.update_existing(self, **data)

mapper(Contact, DB.contacts)
