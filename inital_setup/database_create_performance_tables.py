#!/usr/bin/python3.9

import mysql.connector
from mysql.connector import Error
from datetime import datetime
import sys
import os

import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

DB_HOST = config.DB_HOST
DB_USER = config.DB_USER
DB_PASS = config.DB_PASS
DB_NAME = config.DB_NAME


def create_tables():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )
    cursor = conn.cursor()

    # Create performance_annual table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance_annual (
            id INT AUTO_INCREMENT PRIMARY KEY,
            isin VARCHAR(20),
            year VARCHAR(10),
            start_date DATE,
            end_date DATE,
            annualPerformanceValue DECIMAL(10, 5),
            annualPerformanceBenchmarkValue DECIMAL(10, 5),
            fetched_on DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create performance_trailing_returns table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance_trailing_returns (
            id INT AUTO_INCREMENT PRIMARY KEY,
            isin VARCHAR(20),
            timeframe VARCHAR(20),
            trailingReturnsValue DECIMAL(10, 5),
            trailingReturnsBenchmarkValue DECIMAL(10, 5),
            fetched_on DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Tables created successfully.")
