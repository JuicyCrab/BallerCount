#for storing the personal stats in the database 

import sqlite3

class Stats:
    def __init__(self, db_path="data/stats.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def insert_stats(self, username, date, age, gp, min, fg, fg3, ft, reb, assists, stk, blk, tov, fouls, pts):
        self.cursor.execute("""
            INSERT INTO stats (username, date, age, gp, min, fg, fg3, ft, reb, assists, stk, blk, tov, fouls, pts)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (username, date, age, gp, min, fg, fg3, ft, reb, assists, stk, blk, tov, fouls, pts))
        self.conn.commit()

    def get_stats(self, username):
        self.cursor.execute("SELECT * FROM stats WHERE username = ?", (username))
        return self.cursor.fetchall()

    def get_stats_by_range(self, username, start_date, end_date):
        self.cursor.execute("""
            SELECT * FROM stats
            WHERE username = ? AND date BETWEEN ? AND ?
            ORDER BY date ASC
        """, (username, start_date, end_date))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

    
        
    
        