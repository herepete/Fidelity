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



def wipe_tables(table_name):

    #Wipes all data from the 'all_funds' table.
    try:
        # Connect to the MariaDB database
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Truncate the table (delete all rows)
            truncate_query = f"TRUNCATE TABLE {table_name}"
            cursor.execute(truncate_query)
            connection.commit()
            print(f"The '{table_name}' table has been wiped successfully.")


            #truncate_query = "TRUNCATE TABLE funds_passed"
            #cursor.execute(truncate_query)
            #connection.commit()
            #print("The funds_passed table has been wiped successfully.")


    except Error as e:
        print("Error while connecting to MariaDB:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def remove_tables(table_name):

    if not DB_PASS:
        print("❌ Environment variable DB_PASSWORD is not set.")
        sys.exit(1)

    try:
        # Connect to the MariaDB / MySQL database
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Drop the table
            drop_query = f"DROP TABLE IF EXISTS {table_name}"
            cursor.execute(drop_query)
            connection.commit()
            print(f"✅ The '{table_name}' table has been dropped successfully.")
    except Error as e:
        print(f"❌ Error while connecting to MariaDB: {e}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("🔒 Database connection closed.")

if __name__ == "__main__":
    pass
    #remove_tables(table_name="all_funds_long_list")
