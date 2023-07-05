import mysql.connector
from decouple import config
from passlib.hash import phpass
import datetime
import json


cnxpool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    pool_reset_session=True,
    host=config('DB_HOST'),
    database=config('DB_NAME'),
    user=config('DB_USER'),
    password=config('DB_PASSWORD'),
    port=config('DB_PORT')
)


async def check_user_db(data):
    db = cnxpool.get_connection()
    login = data['login']
    password = data['password']
    print(password)
    cursor = db.cursor()
    query = "SELECT user_login, user_pass  FROM wp_users WHERE user_login = %s AND user_pass = %s"
    values = (login, password)
    cursor.execute(query, values)
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return result is not None


async def verify_hash(data):
    login = data['login']
    password = data['password']
    db = cnxpool.get_connection()
    cursor = db.cursor()
    hash_password = "SELECT user_pass, ID, display_name FROM wp_users WHERE user_login = %s OR user_email = %s"
    values = (login, login)
    cursor.execute(hash_password, values)
    result = cursor.fetchone()
    cursor.close()
    db.close()

    if result is not None:
        hash_value, cmd_id, display_name = result
        compare = phpass.verify(password, hash_value)
        return compare, cmd_id, display_name

    return False, None, None


async def get_user_profile(bot_db):
    db = cnxpool.get_connection()
    cursor = db.cursor()
    profile = "SELECT tarif, end_date, col FROM wp_scoring_col WHERE user_id = %s"
    values = (bot_db,)
    cursor.execute(profile, values)
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return result


async def update_log(user_id, data, json_data):
    db = cnxpool.get_connection()
    cursor = db.cursor()
    upload = """INSERT INTO wp_scoring (user_id, date, ogrn, json) VALUES (%s, %s, %s, %s)"""
    data_user = (user_id[0], datetime.datetime.now(), data, json.dumps(json_data, ensure_ascii=False),)
    cursor.execute(upload, data_user)
    db.commit()
    cursor.close()
    db.close()


async def check_log(u_id):
    db = cnxpool.get_connection()
    cursor = db.cursor()
    query = "SELECT * FROM wp_scoring WHERE user_id = %s ORDER BY date DESC"
    cursor.execute(query, (u_id,))
    log = cursor.fetchall()
    cursor.close()
    db.close()
    return log


async def count_scoring(user_id):
    db = cnxpool.get_connection()
    cursor = db.cursor()
    query = "SELECT COUNT(*) FROM wp_scoring WHERE user_id = %s " \
            "AND YEAR(date) = YEAR(CURRENT_DATE()) AND MONTH(date) = MONTH(CURRENT_DATE())"
    cursor.execute(query, (user_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    db.close()
    return count


async def get_user_email_full_name(u_id):
    try:
        db = cnxpool.get_connection()
        cursor = db.cursor()
        query = f"SELECT user_email, display_name FROM wp_users WHERE ID = %s"
        cursor.execute(query, (u_id,))
        values = cursor.fetchone()
        cursor.close()
        db.close()
        return values
    except:
        return None


async def get_user_phone(u_id):
    try:
        db = cnxpool.get_connection()
        cursor = db.cursor()
        query = "SELECT DISTINCT meta_value FROM wp_usermeta WHERE user_id = %s " \
                "AND meta_key IN ('phone_number')"
        cursor.execute(query, (u_id,))
        values = cursor.fetchone()
        cursor.close()
        db.close()
        return values
    except:
        return None


async def get_user_org(u_id):
    try:
        db = cnxpool.get_connection()
        cursor = db.cursor()
        query = "SELECT DISTINCT meta_value FROM wp_usermeta WHERE user_id = %s " \
                "AND meta_key IN ('org_name')"
        cursor.execute(query, (u_id,))
        values = cursor.fetchone()
        cursor.close()
        db.close()
        return values
    except:
        return None