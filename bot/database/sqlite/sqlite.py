import sqlite3

db = sqlite3.connect('bot_sqlite3')
cur = db.cursor()


async def connect() -> None:
    cur.execute("""CREATE TABLE IF NOT EXISTS bot_user(
    user_id INTEGER NOT NULL UNIQUE,
    login TEXT NOT NULL UNIQUE,
    password TEXT NULL)""")
    db.commit()


async def add_user(user_id, data) -> None:
    cur.execute("""INSERT INTO bot_user VALUES (?, ?, ?)""", (user_id, data.get('login'), data.get('password'),))
    db.commit()


async def user_status(user_id):
    status = cur.execute("""SELECT * FROM bot_user WHERE user_id=?""", (user_id,)).fetchone()
    return status


async def delete_user(user_id) -> None:
    cur.execute("""DELETE FROM bot_user WHERE user_id=?""", (user_id,))
    db.commit()
