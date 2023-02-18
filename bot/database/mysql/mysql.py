import mysql.connector
from decouple import config
from passlib.hash import phpass
from bot.database.sqlite import sqlite
import datetime

db = mysql.connector.connect(
    host=config('DB_HOST'),
    user=config('DB_USER'),
    password=config('DB_PASSWORD'),
    database=config('DB_NAME')
)


async def check_user_db(data):
    login = data['login']
    password = data['password']
    print(password)
    cursor = db.cursor()
    query = "SELECT user_login, user_pass  FROM wp_users WHERE user_login = %s AND user_pass = %s"
    values = (login, password)
    cursor.execute(query, values)
    result = cursor.fetchone()
    cursor.close()
    return result is not None


async def verify_hash(data):
    login = data['login']
    password = data['password']

    try:
        cursor = db.cursor()
        hash_password = "SELECT user_pass, ID FROM wp_users WHERE user_login = %s"
        values = (login,)
        cursor.execute(hash_password, values)
        result = cursor.fetchone()
        cursor.close()
        cmd_id = result[1]
        compare = phpass.verify(password, result[0])
        return compare, cmd_id
    except:
        cursor = db.cursor()
        hash_password = "SELECT user_pass, ID FROM wp_users WHERE user_email = %s"
        values = (login,)
        cursor.execute(hash_password, values)
        result = cursor.fetchone()
        cursor.close()
        cmd_id = result[1]
        compare = phpass.verify(password, result[0])
        return compare, cmd_id


async def get_user_profile(bot_db):
    cursor = db.cursor()
    profile = "SELECT tarif, end_date, col FROM wp_scoring_col WHERE user_id = %s"
    values = (bot_db,)
    cursor.execute(profile, values)
    result = cursor.fetchone()
    cursor.close()
    return result


async def update_log(user_id, data, json):
    cursor = db.cursor()
    upload = """INSERT INTO wp_scoring (user_id, date, ogrn, json) VALUES (%s, %s, %s, %s)"""
    data_user = (user_id[0], datetime.datetime.now(), data, ''.join(json),)
    print(data)
    print(type(data))
    print(type(json))
    cursor.execute(upload, data_user)
    db.commit()
    cursor.close()
    db.close()
