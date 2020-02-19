import random
import sqlite3

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



class User(object):
    def __init__(self, id):
        self.id = id
        self.word = ''
        self.trans = []
        self.examples = []
        self.quest_num = 0
        self.correct = 0

    def reset(self):
        self.word = ''
        self.trans = []
        self.examples = []
        self.quest_num = 0
        self.correct = 0


    def get_rand_example(self):
        ind = random.randint(0, len(self.examples) -1)
        print("Hell")
        return self.examples[ind]