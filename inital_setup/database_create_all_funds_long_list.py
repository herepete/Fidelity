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
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS all_funds_long_list (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    time TIME,
    fund_name VARCHAR(255),
    isin VARCHAR(20),
    fee DECIMAL(5,2),
    yield DECIMAL(5,2),
    frequency VARCHAR(50),
    y1_annualized DECIMAL(6,2),
    y3_annualized DECIMAL(6,2),
    y5_annualized DECIMAL(6,2),
    last_years_yield DECIMAL(6,2),
    morning_star_rating VARCHAR(10)
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
        cursor.execute(CREATE_TABLE_SQL)
        conn.commit()
        print("✅ Table 'all_funds_long_list' created successfully.")
    except mariadb.Error as e:
        print(f"❌ Error creating table: {e}")
        sys.exit(1)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_table()

