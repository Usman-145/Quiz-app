import sqlite3

# ✅ Create Database & Tables
def create_db():
    conn = sqlite3.connect("quiz_leaderboard.db")
    cursor = conn.cursor()

    # Users table (for authentication)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    # Leaderboard table (to store scores)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            score INTEGER
        )
    """)

    conn.commit()
    conn.close()

# ✅ Register a new user
def register_user(username, password):
    conn = sqlite3.connect("quiz_leaderboard.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# ✅ Authenticate user login
def authenticate_user(username, password):
    conn = sqlite3.connect("quiz_leaderboard.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# ✅ Save leaderboard score
def save_score(username, score):
    conn = sqlite3.connect("quiz_leaderboard.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO leaderboard (username, score) VALUES (?, ?)", (username, score))
    conn.commit()
    conn.close()

# ✅ Get leaderboard scores
def get_leaderboard():
    conn = sqlite3.connect("quiz_leaderboard.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, MAX(score) FROM leaderboard GROUP BY username ORDER BY MAX(score) DESC LIMIT 10")
    leaderboard = cursor.fetchall()
    conn.close()
    return leaderboard

# Initialize database
create_db()
