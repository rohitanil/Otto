import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="user",
        password="password",
        database="research"
    )

def get_cursor():
    conn = get_db_connection()
    return conn, conn.cursor()
