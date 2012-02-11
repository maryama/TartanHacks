
from sqlalchemy import MetaData, Table, Column, Integer, Text, ForeignKey

metadata = MetaData()

groups = Table('groups', metadata,
                    Column('user_id', Integer),
                    Column('group_id', Integer)
                    )

links = Table('links', metadata,
                    Column('group_id', Integer),
                    Column('link_id', Integer)
                    )
link_info = Table('link_info', metadata,
                   Column('link_id', Integer),
                   Column('url', Text),
                   Column('title', Text),
                   Column('twitter_handle', Text)
                  )
                 
group_info  = Table('contacts', metadata,
                    Column('id', Integer, primary_key = True),
                    Column('phone', Integer),
                    Column('email', Text),
                    Column('address', Text),
                    Column('city', Text),
                    Column('state', Text),
                    Column('zip', Text)
                    )
