#!/usr/bin/python3.9

import mysql.connector
import os

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

DB_HOST = config.DB_HOST
DB_USER = config.DB_USER
DB_PASS = config.DB_PASS
DB_NAME = config.DB_NAME


def create_tables():
    conn = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME
    )
    cursor = conn.cursor()

    # Geographical breakdown
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS portfolio_geographical_breakdown (
      id          INT AUTO_INCREMENT PRIMARY KEY,
      isin        VARCHAR(20)   NOT NULL,
      `type`      VARCHAR(64)   NOT NULL,
      `value`     DECIMAL(10,5) DEFAULT NULL,
      fetched_on  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
      INDEX idx_isin   (isin),
      INDEX idx_type   (`type`),
      INDEX idx_value  (`value`)
    )
    """)

    # Individual portfolio holdings
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS portfolio_holdings (
        id            INT AUTO_INCREMENT PRIMARY KEY,
        isin          VARCHAR(20)   NOT NULL,
        security_name VARCHAR(255)  NOT NULL,
        country_id    VARCHAR(64)   DEFAULT NULL,
        industry_id   VARCHAR(64)   DEFAULT NULL,
        weighting     DECIMAL(10,5) DEFAULT NULL,
        fetched_on    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_holdings_isin    (isin),
        INDEX idx_holdings_country (country_id)
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("✅ portfolio_geographical_breakdown & portfolio_holdings tables created (or already exist).")
