import sqlite3
from passlib.hash import phpass

db = sqlite3.connect('bot_sqlite3')
cur = db.cursor()


async def connect() -> None:
    cur.execute("""CREATE TABLE IF NOT EXISTS bot_user(
    u_id INTEGER NOT NULL UNIQUE,
    user_id INTEGER NOT NULL UNIQUE,
    login TEXT NOT NULL UNIQUE,
    password TEXT NULL)""")
    db.commit()


async def add_user(u_id, user_id, data) -> None:
    password = phpass.hash(data.get('password'))
    cur.execute("""INSERT INTO bot_user VALUES (?, ?, ?, ?)""", (u_id, user_id, data.get('login'), password,))
    db.commit()


async def user_status(user_id):
    status = cur.execute("""SELECT * FROM bot_user WHERE user_id=?""", (user_id,)).fetchone()
    return status


async def delete_user(user_id) -> None:
    cur.execute("""DELETE FROM bot_user WHERE user_id=?""", (user_id,))
    db.commit()


async def get_id(user_id):
    u_id = cur.execute("""SELECT u_id FROM bot_user WHERE user_id=?""", (user_id,)).fetchone()
    return u_id
