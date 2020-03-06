from sqlalchemy import Column, ForeignKey, Integer, String, Table, DateTime, create_engine
#from app import db

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Examples(Base):
    __tablename__ = 'Examples'
    id = Column(Integer, primary_key=True)
    sentence = Column(String)
    word_id = Column(Integer, ForeignKey('Words.id'))
    #word = relationship('Words')

    def __str__(self):
        return "{}".format(self.sentence)


class Words(Base):
    __tablename__ = 'Words'
    id = Column(Integer, primary_key=True)
    word = Column(String)
    translation = Column(String)

    def __str__(self):
        return "{}".format(self.name)


class Learning(Base):
    __tablename__ = 'Learning'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'))
    word_id = Column(Integer, ForeignKey('Words.id'))
    correct = Column(Integer)
    date = Column(DateTime)



class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True)
    date = Column(DateTime)
    
    def __repr__(self):
        return '<User %r>' % (self.user_id)
