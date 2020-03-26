from sqlalchemy import Column, ForeignKey, Integer, String, Table, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Examples(Base):
    __tablename__ = 'examples'
    id = Column(Integer, primary_key=True)
    sentence = Column(String)
    word_id = Column(Integer, ForeignKey('words.id'))

    def __str__(self):
        return "{}".format(self.sentence)


class Words(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    word = Column(String)
    translation = Column(String)

    def __str__(self):
        return "{}".format(self.name)


class Learning(Base):
    __tablename__ = 'learning'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    word_id = Column(Integer, ForeignKey('words.id'))
    correct = Column(Integer)
    date = Column(DateTime)



class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True)
    date = Column(DateTime)

    def __repr__(self):
        return '<User %r>' % (self.user_id)

class Settings(Base):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True)
    time = Column(Integer)
    round = Column(Integer)
    cwords = Column(Integer)
    

