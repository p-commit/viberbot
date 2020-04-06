import random
import sqlite3
from datetime import datetime as dt
from datetime import timedelta
import models as m
from app import db


class MyDB(object):

    def add_user(self, id):
        u = m.Users(user_id=id,  date = dt.now(), word = '', trans='', examples ='', quest_num=0, correct =0)
        db.session.add(u)
        db.session.commit()

        w = db.session.query(m.Words).all()
        for word in w:
            l = m.Learning(user_id=u.id, word_id=word.id, correct=0)
            db.session.add(l)
        db.session.commit()
        print('Пользователь добавлен')

    def check_user(self, id):
        u = db.session.query(m.Users).filter(m.Users.user_id == id).all()
        if len(u) > 0:
            print('Пользователь найден')
            return True
        print('Пользователь не найден')
        return False

    def get_settings(self):
        settings = db.session.query(m.Settings).first()
        return settings
    
    def get_user(self,id):
        u = db.session.query(m.Users).filter(m.Users.user_id == id).first()
        return u

    def get_question(self, id):
        cor = 15
        res = []
        user = db.session.query(m.Users).filter(m.Users.user_id == id).first()
        user.quest_num +=1

        words = db.session.query(m.Learning, m.Words).filter(
            m.Learning.user_id == user.id, m.Learning.correct < cor)
        words = words.join(m.Learning, m.Learning.word_id == m.Words.id).all()
        words = random.sample(words, 4)
        
        user.word = words[0][1].word

        w = ''
        for elem in words:
            w+= elem[1].translation +'%'       
        w = w[0:len(w)-1]
        user.trans = w


        ex = db.session.query(m.Examples).filter(
            m.Examples.word_id == words[0][1].id).all()
        e = ''
        for elem in ex:
            e += elem.sentence + '%'
        e = e[0:len(e)-1]
        user.examples = e
       
        db.session.commit()

    def correct_answer(self, id, word):
        user = db.session.query(m.Users).filter(m.Users.user_id == id).first()
        user.correct +=1
        self.update_answer_date(id)

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


    def set_settings(self, time, round, cwords):
        settings = db.session.query(m.Settings).first()
        settings.time = time
        settings.round = round
        settings.cwords = cwords
        db.session.commit()

    def get_user_info(self, id):

        date = db.session.query(m.Users).filter(m.Users.user_id == id).first()
 
        last_answer_date = date.date

        words = db.session.query(m.Words).all()
        words_count = len(words)

        s = db.session.query(m.Settings).first()

        learn_words = db.session.query(m.Learning).filter(m.Learning.correct > s.cwords).all()
        learn = len(learn_words)

        return (learn, words_count, last_answer_date)

    def user_reset(self, id):
        u = db.session.query(m.Users).filter(m.Users.user_id == id).first()
        u.word = ''
        u.trans = ''
        u.examples =''
        u.quest_num = 0
        u.correct = 0
        db.session.commit()

mydb = MyDB()
