#!/usr/bin/python3.9

import mysql.connector
from mysql.connector import Error
from datetime import datetime
import sys

import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

DB_HOST = config.DB_HOST
DB_USER = config.DB_USER
DB_PASS = config.DB_PASS
DB_NAME = config.DB_NAME

# === SQL to create the table ===
create_table_sql = """
CREATE TABLE IF NOT EXISTS growth (
    id INT AUTO_INCREMENT PRIMARY KEY,
    isin VARCHAR(20),
    period VARCHAR(5),
    endDate DATE,
    value DECIMAL(10, 4),
    fetched_on DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""



def create_table():
    try:
        conn = mysql.connector.connect(
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        conn.commit()
        print("✅ Table 'growth table' created successfully.")
    except Exception as e:
        print(f"❌ Error creating table: {e}")
        sys.exit(1)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_table()

