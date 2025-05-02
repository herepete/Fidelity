#!/usr/bin/python3.9

import os
import sys
import mysql.connector
from mysql.connector import Error

# Import your functions
from database_drop_and_truncate import wipe_tables, remove_tables
from query_databases import query_any_database
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'inital_setup')))
from database_health_check import     run_db_health_check
from database_health_check import check_disk_space
from  query_databases import list_and_describe_tables



import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

DB_HOST = config.DB_HOST
DB_USER = config.DB_USER
DB_PASS = config.DB_PASS
DB_NAME = config.DB_NAME



import subprocess
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'troubleshooting_tools')))
import setup_check


def list_tables():
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
        return tables

    except Error as e:
        print(f"❌ Error listing tables: {e}")
        return []

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def show_menu(table_name):
    while True:
        print(f"\n📘 Selected Table: {table_name}")
        print("1) Drop Table")
        print("2) Truncate Table")
        print("3) Insert Sample Data")
        print("4) Query Table")
        print("5) Back to Table List")
        choice = input("Choose an option: ")

        if choice == "1":
            remove_tables(table_name)
        elif choice == "2":
            wipe_tables(table_name)
        elif choice == "3":
            # For testing, you can replace with dynamic input later
            from datetime import datetime
            sample_data = [[
                datetime.today().date(), datetime.now().time(), "Sample Fund", "ISIN000X", 0.20, 4.8, "Monthly",
                3.5, 5.0, 6.0, 4.7, "3"
            ]]
            insert_funds(sample_data)
        elif choice == "4":
            query_any_database(dbname=table_name)
        elif choice == "5":
            break
        else:
            print("❗ Invalid choice. Try again.")

def main():
    if not DB_PASS:
        print("❌ DB_PASSWORD not set in environment.")
        sys.exit(1)

    while True:
        print("\n==== Useful Stuff ====")
        print("""mysql -u root -e "use investment_db ; show tables;desc fidelity_insights " -p""")
        print ("""mysql -u root -e "SELECT    table_name,    table_rows AS approx_row_count  FROM information_schema.tables  WHERE table_schema = 'investment_db'" -p""")
        print ("""du -sh ./* /var/lib/mysql""")


        print("\n==== DATABASE CLI ====")
        tables = list_tables()
        if not tables:
            print("No tables found.")
            break
        print("\n==== Tables Found ====")
        for i, table in enumerate(tables):
            print(f"{i + 1}) {table}")
        print("\n==== Other Actions ====")
        print("97) Run System Checks")
        print("98) Run Database Health Check")
        print("99) Run a Desc on Each table")
        print("0) Exit")

        try:
            selection = int(input("Select a table: "))
            if selection == 0:
                break
            elif selection == 97:
                setup_check.project_status()
            elif selection == 98:
                run_db_health_check()
                check_disk_space()
            elif selection == 99:
                list_and_describe_tables()
            elif 1 <= selection <= len(tables):
                show_menu(tables[selection - 1])
            else:
                print("❗ Invalid selection. Try again.")
        except ValueError:
            print("❗ Please enter a number.")

if __name__ == "__main__":
    main()

