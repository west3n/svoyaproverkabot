import mysql.connector
from decouple import config

db = mysql.connector.connect(
    host=config('DB_HOST'),
    user=config('DB_USER'),
    password=config('DB_PASSWORD'),
    database=config('DB_NAME')
)


async def check_user_db(data):
    login = data['login']
    password = data['password']
    cursor = db.cursor()
    query = "SELECT * FROM users WHERE login = %s AND password = %s"
    values = (login, password)
    cursor.execute(query, values)
    result = cursor.fetchone()
    cursor.close()
    return result is not None
