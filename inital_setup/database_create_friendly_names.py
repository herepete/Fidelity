#!/usr/bin/python3.9
import mysql.connector
from mysql.connector import Error

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

DB_HOST = config.DB_HOST
DB_USER = config.DB_USER
DB_PASS = config.DB_PASS
DB_NAME = config.DB_NAME

def create_friendly_names_table():
    try:
        conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS friendly_names (
                id            INT AUTO_INCREMENT PRIMARY KEY,
                isin          VARCHAR(20)   NOT NULL,
                fund_type          VARCHAR(120)   NOT NULL,
                friendly_name VARCHAR(255)  NOT NULL,
                fetch_date    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_fn_isin (isin)
            )
        """)
        conn.commit()
        print("✅ Table `friendly_names` created successfully.")
    except Error as e:
        print(f"❌ Error creating table: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    create_friendly_names_table()

