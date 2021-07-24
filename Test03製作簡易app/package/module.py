from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Information(Base):
    __tablename__ = 'information'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(40))
    second_name = Column(String(40))
    email = Column(String(60))

    def __init__(self, first_name, second_name, email):
        self.first_name = first_name
        self.second_name = second_name
        self.email = email

def show_all():
    engine = create_engine('sqlite:///database/student.db?check_same_thread=False', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    data = session.query(Information).all()
    for i in range(len(data)):
        print(data[i].id, ' ', data[i].first_name, data[i].second_name, data[i].email)
    session.close()

def add_one(first_name, second_name, email):
    engine = create_engine('sqlite:///database/student.db?check_same_thread=False', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(Information(first_name, second_name, email))
    session.commit()
    session.close()

def add_many(list):
    engine = create_engine('sqlite:///database/student.db?check_same_thread=False', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    for a, b, c in list:
        session.add(Information(a, b, c))
    session.commit()
    session.close()

def email_lookup(email):
    engine = create_engine('sqlite:///database/student.db?check_same_thread=False', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    data = session.query(Information).filter(Information.email == email).all()
    for i in range(len(data)):
        print(data[i].id, ' ', data[i].first_name, data[i].second_name, data[i].email)
    session.close()

def delete_one(id):
    engine = create_engine('sqlite:///database/student.db?check_same_thread=False', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.query(Information).filter(Information.id == id).delete()
    session.commit()
    session.close()

def update_first_name(email, first_name):
    engine = create_engine('sqlite:///database/student.db?check_same_thread=False', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    data1 = session.query(Information).filter(Information.email == email).first()
    print(data1.id, ' ', data1.first_name, data1.second_name, data1.email)
    session.query(Information).filter(Information.email == email).update({Information.first_name : first_name})
    session.commit()
    data2 = session.query(Information).filter(Information.email == email).first()
    print(data2.id, ' ', data2.first_name, data2.second_name, data1.email)

def update_second_name(email, second_name):
    engine = create_engine('sqlite:///database/student.db?check_same_thread=False', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    data1 = session.query(Information).filter(Information.email == email).first()
    print(data1.id, ' ', data1.first_name, data1.second_name, data1.email)
    session.query(Information).filter(Information.email == email).update({Information.second_name : second_name})
    session.commit()
    data2 = session.query(Information).filter(Information.email == email).first()
    print(data2.id, ' ', data2.first_name, data2.second_name, data1.email)

def update_email(old_email, new_email):
    engine = create_engine('sqlite:///database/student.db?check_same_thread=False', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    data1 = session.query(Information).filter(Information.email == old_email).first()
    print(data1.id, ' ', data1.first_name, data1.second_name, data1.email)
    session.query(Information).filter(Information.email == old_email).update({Information.email : new_email})
    session.commit()
    data2 = session.query(Information).filter(Information.email == new_email).first()
    print(data2.id, ' ', data2.first_name, data2.second_name, data1.email)
