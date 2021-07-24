# Python3 + SQLAlchemy + Sqlite3 實現 ORM 教程
# 參考網站
# https://www.cnblogs.com/lsdb/p/9835894.html
# https://www.itread01.com/content/1546084449.html
# https://codertw.com/%E8%B3%87%E6%96%99%E5%BA%AB/10142/
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///test.db?check_same_thread=False', echo=True)

metadata = MetaData(engine)

user = Table('test_user', metadata,
    Column('id', Integer, primary_key = True),
    Column('first_name', String(40)),
    Column('second_name', String(40)),
    Column('email', String(60)))

metadata.create_all(engine)

Base = declarative_base()

class TestUser(Base):
    __tablename__ = 'test_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(40))
    second_name = Column(String(40))
    email = Column(String(60))

    def __init__(self, first_name, second_name, email):
        self.first_name = first_name
        self.second_name = second_name
        self.email = email

Session = sessionmaker(bind=engine)
session01 = Session()
session01.close()