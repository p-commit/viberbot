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
                                FOREIGN KEY(word_id) references words(id))"\
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


#create_tables(conn)
fill_tables(conn)
cursor = conn.cursor()
cursor.execute("SELECT word, translation FROM words")
words = cursor.fetchall()
print(words)