
from sqlalchemy import MetaData, Table, Column, Integer, Text, ForeignKey

metadata = MetaData()

user_accounts = Table('users', metadata,
                    Column('username', Text, primary_key=True),
                    Column('password', Text),
                    Column('contact_id', Integer, ForeignKey('contacts.id')),
                    Column('group', Text),
                    )

students = Table('students', metadata,
                 Column('username', Text, ForeignKey('users.username'), primary_key = True),
                 Column('lname', Text),
                 Column('fname', Text),
                 Column('mname', Text),
                 Column('qualifications', Text),
                 Column('pos_hours', Text)
                 )

employers = Table('employers', metadata,
                   Column('username', Text, ForeignKey('users.username'), primary_key = True)
                  )
                 

contacts = Table('contacts', metadata,
                    Column('id', Integer, primary_key = True),
                    Column('phone', Integer),
                    Column('email', Text),
                    Column('address', Text),
                    Column('city', Text),
                    Column('state', Text),
                    Column('zip', Text)
                    )


#jobs = Table('jobs', metadata)

#candidates = Table('candidates', metadata)

#employees = Table('employees', metadata)


