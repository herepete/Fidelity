#!/usr/bin/python3.9

import os
import mysql.connector
from mysql.connector import Error

import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

DB_HOST = config.DB_HOST
DB_USER = config.DB_USER
DB_PASS = config.DB_PASS
DB_NAME = config.DB_NAME


def create_tables():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        cursor = conn.cursor()

        # Summary table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dividends (
            id                    INT AUTO_INCREMENT PRIMARY KEY,
            isin                  VARCHAR(20)    NOT NULL,
            is_primary            BOOLEAN        DEFAULT NULL,
            distribution_yield    DECIMAL(10,5)  DEFAULT NULL,
            historic_yield        DECIMAL(10,5)  DEFAULT NULL,
            underlying_yield      DECIMAL(10,5)  DEFAULT NULL,
            frequency             VARCHAR(32)    DEFAULT NULL,
            latest_payment_date   DATE           DEFAULT NULL,
            fetched_on            DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_div_isin    (isin)
        );
        """)

        # History table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dividend_history (
            id                      INT AUTO_INCREMENT PRIMARY KEY,
            isin                    VARCHAR(20)     NOT NULL,
            pay_date                DATE            DEFAULT NULL,
            reinvestment_price      DECIMAL(12,5)   DEFAULT NULL,
            per_share_amount        DECIMAL(12,5)   DEFAULT NULL,
            fetched_on              DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_hist_isin     (isin)
        );
        """)

        conn.commit()
        print("✅ Dividend tables created successfully.")
    except Error as e:
        print(f"❌ Error creating tables: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    create_tables()

