import random
import sqlite3
from datetime import datetime as dt

class MyDB(object):
    def __init__(self):
        self.connection = sqlite3.connect("project.db", check_same_thread = False)


    def add_user(self, id):
        cur = self.connection.cursor()
        cur.execute("INSERT INTO users(user_id) VALUES(?)", (id,))

        cur.execute("SELECT id FROM words")
        words_ind = cur.fetchall()
        
        for elem in words_ind:
            cur.execute("INSERT INTO learning(user_id, word_id, correct)\
                            VALUES(?, ?, ?)", (id, elem[0], 0))
        self.connection.commit()
    
    def check_user(self, id):
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", (id,))
        
        if len(cur.fetchall()) == 0:
            return False
        else:
            return True

    def get_user(self, id):
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", (id,))
        user_id  = cur.fetchone()
        return user_id

    def get_question(self, id):
        cur = self.connection.cursor()
        cur.execute("SELECT words.id, translation, word\
                        FROM learning \
                        JOIN words \
                            ON learning.word_id = words.id\
                        WHERE user_id = ? AND correct < ?\
                            ORDER BY RANDOM() LIMIT 4", (id, 20))
        words = cur.fetchall()
        
        cur.execute("SELECT sentence\
                        FROM examples\
                        WHERE word_id = ?", (words[0][0],))
        examples = cur.fetchall()
        
        for elem in examples:
            words.append(elem)
        
        return words

    def correct_answer(self, id, word):
        cur = self.connection.cursor()
        cur.execute("SELECT words.id, correct, date\
                        FROM learning\
                        JOIN words\
                            ON words.id = learning.word_id\
                    WHERE user_id = ? AND translation = ?", (id, word))
        word_learn = cur.fetchone()
            
        cur.execute("UPDATE learning \
                        SET correct = ?, date = ?\
                        WHERE user_id = ? AND word_id = ?", (word_learn[1]+1, dt.now(), id, word_learn[0]))
        self.connection.commit()

        print(word_learn)





class User(object):
    def __init__(self, id):
        self.id = id
        self.word = ''
        self.trans = []
        self.examples = []
        self.quest_num = 0
        self.correct = 0

    def get_question(self):
        quest = db.get_question(self.id)
        
        self.word = quest[0][1]

        for i in range(0,4):
            self.trans.append(quest[i][2])
        
        for i in range(4, len(quest)-1):
            self.examples.append(quest[i][0])

    def reset(self):
        self.word = ''
        self.trans = []
        self.examples = []
        self.quest_num = 0
        self.correct = 0


    def get_rand_example(self):
        ind = random.randint(0, len(self.examples) -1)
        return self.examples[ind]


db = MyDB()