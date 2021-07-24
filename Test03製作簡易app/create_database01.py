from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database/student.db?check_same_thread=False', echo=False)

metadata = MetaData(engine)

user = Table('information', metadata,
    Column('id', Integer, primary_key = True),
    Column('first_name', String(40)),
    Column('second_name', String(40)),
    Column('email', String(60)))

metadata.create_all(engine)

Base = declarative_base()
