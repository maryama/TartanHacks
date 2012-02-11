
from sqlalchemy import MetaData, Table, Column, Integer, Text, ForeignKey

metadata = MetaData()

groups = Table('groups', metadata,
                    Column('user_id', Integer, primary_key= True),
                    Column('group_id', Integer, primary_key = True)
                    )

links = Table('links', metadata,
                    Column('group_id', Integer, primary_key=True),
                    Column('link_id', Integer, primary_key=True)
                    )
link_info = Table('link_info', metadata,
                   Column('link_id', Integer, primary_key=True),
                   Column('url', Text),
                   Column('title', Text),
                   Column('twitter_handle', Text)
                  )
                 
group_info  = Table('group_info', metadata,
                    Column('group_id', Integer, primary_key = True),
                    Column('name', Text),
                    Column('num_links', Integer),
                    )
