import sqlite3

DB_NAME = "books.db"

def connect():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT,
        category TEXT
    )
    """)

    conn.commit()
    conn.close()

def add_book(title, author, category):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO books (title, author, category) VALUES (?, ?, ?)",
        (title, author, category)
    )

    conn.commit()
    conn.close()

def get_books():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT title, author, category FROM books")
    rows = cur.fetchall()

    conn.close()
    return rows

def get_books_by_category(category):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT title, author, category FROM books WHERE category = ?",
        (category,)
    )
    rows = cur.fetchall()

    conn.close()
    return rows

def search_books(keyword):
    conn = connect()
    cur = conn.cursor()

    like = f"%{keyword}%"
    cur.execute("""
        SELECT title, author, category
        FROM books
        WHERE title LIKE ? OR author LIKE ?
    """, (like, like))

    rows = cur.fetchall()
    conn.close()
    return rows

def delete_book(title, author, category):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM books WHERE title=? AND author=? AND category=?",
        (title, author, category)
    )

    conn.commit()
    conn.close()


def update_book(old_title, old_author, old_category, new_title, new_author, new_category):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        UPDATE books
        SET title=?, author=?, category=?
        WHERE title=? AND author=? AND category=?
    """, (new_title, new_author, new_category,
          old_title, old_author, old_category))

    conn.commit()
    conn.close()
