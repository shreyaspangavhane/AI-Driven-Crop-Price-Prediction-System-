# utils/db_connection.py

import mysql.connector
from datetime import datetime

def connect_db():
    """Connects to the MySQL database and returns the connection."""
    conn = mysql.connector.connect(
        host='localhost',
        user='root',  # Change this to your MySQL username
        password='',  # Change this to your MySQL password
        database='agriculture_db'  # Database name
    )
    return conn

def fetch_crop_data():
    """Fetches crop data from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM crop_table")  # Adjust table name as needed
    result = cursor.fetchall()
    conn.close()
    return result

def insert_crop_data(state, district, market, commodity, variety, grade, arrival_date, min_price, max_price, modal_price):
    """Inserts crop data into the database."""
    conn = connect_db()
    cursor = conn.cursor()
    query = """
        INSERT INTO crop_table (state, district, market, commodity, variety, grade, arrival_date, min_price, max_price, modal_price)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (state, district, market, commodity, variety, grade, arrival_date, min_price, max_price, modal_price))
    conn.commit()
    conn.close()
    print("✅ Data inserted successfully into the database!")
