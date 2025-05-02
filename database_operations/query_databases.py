#!/usr/bin/python3.9

import mysql.connector
from mysql.connector import Error
import os
import sys
from tabulate import tabulate


# === CONFIG ===

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

DB_HOST = config.DB_HOST
DB_USER = config.DB_USER
DB_PASS = config.DB_PASS
DB_NAME = config.DB_NAME


def query_any_database(dbname):
    if not DB_PASS:
        print("❌ Environment variable DB_PASSWORD is not set.")
        sys.exit(1)

    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {dbname}")
            rows = cursor.fetchall()

            print(f"\n✅ Retrieved {len(rows)} rows from {dbname}:\n")
            for row in rows:
                print(row)

    except Error as e:
        print(f"❌ Error while fetching data: {e}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("\n🔒 Database connection closed.")


def list_and_describe_tables():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES;")
        tables = [row[0] for row in cursor.fetchall()]

        for table in tables:
            print(f"\n🟦 Table: {table}")
            cursor.execute(f"DESCRIBE {table};")
            columns = cursor.fetchall()
            headers = ["Field", "Type", "Null", "Key", "Default", "Extra"]
            print(tabulate(columns, headers=headers, tablefmt="grid"))

    except Error as e:
        print(f"❌ Error: {e}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    #list_and_describe_tables()
    pass
    #query_database(dbname)

