import random
import sqlite3
from datetime import datetime as dt
from datetime import timedelta
import models as m
from app import db


class MyDB(object):

    def add_user(self, id):
        u = m.Users(user_id=id)
        db.session.add(u)

        w = db.session.query(m.Words).all()
        for word in w:
            l = m.Learning(user_id=id, word_id=word.id, correct=0)
            db.session.add(l)

        db.session.commit()

    def check_user(self, id):
        u = db.session.query(m.Users).filter(m.Users.user_id == id).all()
        if len(u) > 0:
            return True
        return False

    def get_question(self, id):
        cor = 5
        res = []
        user = db.session.query(m.Users).filter(m.Users.user_id == id).first()
        
        words = db.session.query(m.Learning, m.Words).filter(
            m.Learning.user_id == user.id, m.Learning.correct < cor)
        words = words.join(m.Learning, m.Learning.word_id == m.Words.id).all()
        words = random.sample(words, 4)

        for elem in words:
            res.append(elem[1])

        ex = db.session.query(m.Examples).filter(
            m.Examples.word_id == words[0][1].id).all()
        for elem in ex:
            res.append(elem.sentence)

        return res

    def correct_answer(self, id, word):
        user = db.session.query(m.Users).filter(m.Users.user_id == id).first()
        
        words = db.session.query(m.Learning, m.Words).filter(
            m.Learning.user_id == user.id, m.Words.translation == word)
        words = words.join(m.Learning, m.Learning.word_id == m.Words.id).all()
        words[0][0].correct += 1
        words[0][0].date = dt.now()
        db.session.commit()

    def update_answer_date(self, id):
        user = db.session.query(m.Users).filter(m.Users.user_id == id).first()
        user.date = dt.now()
        db.session.commit()


    def get_user_info(self, id):

        date = db.session.query(m.Users).filter(m.Users.user_id == id).first()
 
        last_answer_date = date.date

        words = db.session.query(m.Words).all()
        words_count = len(words)

        learn_words = db.session.query(m.Learning).filter(
            m.Learning.user_id == date.id, m.Learning.correct > 5).all()
        learn = len(learn_words)

        return (learn, words_count, last_answer_date)


mydb = MyDB()


class User(object):
    def __init__(self, id):
        self.id = id
        self.word = ''
        self.trans = []
        self.examples = []
        self.quest_num = 0
        self.correct = 0

    def get_question(self):
        self.quest_num += 1
        self.trans = []
        self.examples = []
        quest = mydb.get_question(self.id)

        self.word = quest[0].word
        for i in range(0, 4):
            self.trans.append(quest[i].translation)

        for i in range(4, len(quest)-1):
            self.examples.append(quest[i])

    def reset(self):
        self.word = ''
        self.trans = []
        self.examples = []
        self.quest_num = 0
        self.correct = 0

    def update_date(self):
        mydb.update_answer_date(self.id)

    def correct_ans(self):
        self.correct += 1
        mydb.correct_answer(self.id, self.trans[0])

    def get_rand_example(self):
        ind = random.randint(0, len(self.examples) - 1)
        return self.examples[ind]
