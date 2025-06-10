#for the login and signup 
import sqlite3

db_path = "data/auth.db"

def connect():
    return sqlite3.connect(database=db_path)

def create_users_table():
    conn = sqlite3.connect(database=db_path)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE if NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username NOT NULL UNIQUE,
            password NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect(database=db_path)
    cursor = conn.cursor()
    try: 
        cursor.execute("INSERT into users (username, password) VALUES (?,?)",(username,password))
        conn.commit()
        return True
        12123
    except sqlite3.IntegrityError: 
        return False 
    
    finally:
        conn.close() 

def login_user(username, password):
    conn = sqlite3.connect(database=db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?",(username,password))
    result = cursor.fetchone()
    conn.close()
    return result is not None


    