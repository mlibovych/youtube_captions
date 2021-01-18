import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("film_captions.db")
        self.cursor = self.conn.cursor()

        sql = """CREATE TABLE IF NOT EXISTS films
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, done INTEGER)
                        """
        self.cursor.execute(sql)

        sql = """CREATE TABLE IF NOT EXISTS captions
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, film_id INTEGER, code TEXT, 
                    video_duration time(7), request INTEGER, position INTEGER, file_name TEXT,
                    FOREIGN KEY (film_id) REFERENCES films(id))
                """

        self.cursor.execute(sql)

        self.conn.commit()

    def insert_caption(self, film_id, code, video_duration, request, position, file_name):
        sql = """INSERT INTO captions (film_id, code, video_duration, request, position, file_name)
                    VALUES (?, ?,?,?,?,?)
                """

        self.cursor.execute(sql, [film_id, code, video_duration, request, position, file_name])

        sql = """ CREATE INDEX IF NOT EXISTS film_id_index ON films(id)"""

        self.cursor.execute(sql)

        self.conn.commit()

        sql = """SELECT last_insert_rowid()"""

        self.cursor.execute(sql)

        return self.cursor.fetchone()

    def insert_film(self, film):
        sql = """INSERT INTO films (title, done)
                    VALUES (?, 0)
                """

        self.cursor.execute(sql, [film])

        self.conn.commit()

        sql = """SELECT last_insert_rowid()"""

        self.cursor.execute(sql)

        return self.cursor.fetchone()

    def update_film(self, film_id, done):
        sql = """UPDATE films  SET done = ?  WHERE id = ?"""

        self.cursor.execute(sql, [done, film_id,])

        self.conn.commit()

    def get_not_proceeded_films(self):
        sql = """SELECT id, title FROM films  WHERE done = 0"""

        self.cursor.execute(sql)

        return self.cursor.fetchall()
