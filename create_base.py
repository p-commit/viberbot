import sqlite3
 
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

create_tables(conn)