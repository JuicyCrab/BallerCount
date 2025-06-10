import sqlite3

db_path = "data/stats.db"
conn = sqlite3.connect(database=db_path)
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                date TEXT,
                age INTEGER,
                gp INTEGER,
                min INTEGER,
                fg REAL,
                fg3 REAL,
                ft REAL,
                reb INTEGER,
                assists INTEGER,
                stk INTEGER,
                blk INTEGER,
                tov INTEGER,
                fouls INTEGER,
                pts INTEGER,
                FOREIGN KEY (username) REFERENCES users(email)
           ) """
)
conn.commit()
conn.close()