import mysql.connector
from decouple import config

db = mysql.connector.connect(
    host=config('DB_HOST'),
    user=config('DB_USER'),
    password=config('DB_PASSWORD'),
    database=config('DB_NAME')
)


async def create_user_db(data):
    login = data['login']
    password = data['password']
    cursor = db.cursor()
    query = "INSERT INTO users (login, password) VALUES (%s, %s)"
    values = (login, password)
    cursor.execute(query, values)
    db.commit()
    cursor.close()
    db.close()
