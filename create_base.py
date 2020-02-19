import sqlite3
import json
 
conn = sqlite3.connect("project.db")

def create_tables(con):
    cursor = con.cursor()
    cursor.execute(
        "CREATE TABLE words(id INTEGER PRIMARY KEY,\
                                word VARCHAR, \
                                translation VARCHAR)"
        )

    cursor.execute(
        "CREATE TABLE examples(id INTEGER PRIMARY KEY,\
                                sentence VARCHAR,\
                                word_id INTEGER,\
                                FOREIGN KEY(word_id) references words(id))"
        )

    cursor.execute(
        "CREATE TABLE learning(id INTEGER PRIMARY KEY,\
                                user_id VARCHAR,\
                                word_id INTEGER,\
                                correct INTEGER,\
                                date DATETIME,\
                                FOREIGN KEY(word_id) references words(id),\
                                FOREIGN KEY(user_id) references users(id))"
        )

    cursor.execute(
        "CREATE TABLE users(id INTEGER PRIMARY KEY,\
                                user_id VARCHAR,\
                                date DATETIME)"
        )

    con.commit()


def fill_tables(con):
    with open('english_words.json', 'r', encoding='utf-8') as english_words:
        words = json.load(english_words)
        
        cursor = con.cursor()
        
        i = 0
        for elem in words:           
            i+= 1
            cursor.execute('''INSERT INTO words(word, translation)\
                                 VALUES(?, ?)''', (elem['word'], elem['translation']) )
            
            for ex in elem['examples']:
                cursor.execute('''INSERT INTO examples(sentence, word_id)\
                                 VALUES(?, ?)''', (ex, i) )
        
        con.commit()


create_tables(conn)
fill_tables(conn)
