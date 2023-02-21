import mysql.connector
from decouple import config
from passlib.hash import phpass
import datetime
import json

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

    cursor = db.cursor()
    hash_password = "SELECT user_pass, ID, display_name FROM wp_users WHERE user_login = %s OR user_email = %s"
    values = (login, login)
    cursor.execute(hash_password, values)
    result = cursor.fetchone()
    cursor.close()

    if result is not None:
        hash_value, cmd_id, display_name = result
        compare = phpass.verify(password, hash_value)
        return compare, cmd_id, display_name

    return False, None, None


async def get_user_profile(bot_db):
    cursor = db.cursor()
    profile = "SELECT tarif, end_date, col FROM wp_scoring_col WHERE user_id = %s"
    values = (bot_db,)
    cursor.execute(profile, values)
    result = cursor.fetchone()
    cursor.close()

    return result


async def update_log(user_id, data, json_data):
    cursor = db.cursor()
    upload = """INSERT INTO wp_scoring (user_id, date, ogrn, json) VALUES (%s, %s, %s, %s)"""
    data_user = (user_id[0], datetime.datetime.now(), data, json.dumps(json_data, ensure_ascii=False),)
    cursor.execute(upload, data_user)
    db.commit()
    cursor.close()


async def check_log(u_id):
    cursor = db.cursor()
    query = "SELECT * FROM wp_scoring WHERE user_id = %s ORDER BY date DESC"
    cursor.execute(query, (u_id,))
    log = cursor.fetchall()
    cursor.close()
    return log


async def count_scoring(user_id):
    cursor = db.cursor()
    query = "SELECT COUNT(*) FROM wp_scoring WHERE user_id = %s " \
            "AND YEAR(date) = YEAR(CURRENT_DATE()) AND MONTH(date) = MONTH(CURRENT_DATE())"
    cursor.execute(query, (user_id,))
    count = cursor.fetchone()[0]
    cursor.close()

    return count
