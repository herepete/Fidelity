#!/usr/bin/python3.9

import os
import mysql.connector
from mysql.connector import Error

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

DB_HOST = config.DB_HOST
DB_USER = config.DB_USER
DB_PASS = config.DB_PASS
DB_NAME = config.DB_NAME


def create_tables():
    conn = None
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS risk_and_rating_data (
                id                       INT AUTO_INCREMENT PRIMARY KEY,
                isin                     VARCHAR(20)   NOT NULL,
                time_period              VARCHAR(10)   DEFAULT NULL,
                rating_value             INT           DEFAULT NULL,
                risk_rating_value        VARCHAR(32)   DEFAULT NULL,
                performance_rating_value VARCHAR(32)   DEFAULT NULL,
                fetched_on               DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_rar_isin        (isin),
                INDEX idx_rar_time_period (time_period)
            )
        """)
        conn.commit()
        print("✅ Table `risk_and_rating_data` created successfully.")
    except Error as e:
        print(f"❌ Error creating table: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    create_tables()

