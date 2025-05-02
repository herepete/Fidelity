#!/usr/bin/python3.9

import os
import sys
import mysql.connector
from mysql.connector import Error

# Import your functions
from database_drop_and_truncate import wipe_tables, remove_tables
from query_databases import query_any_database
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'inital_setup')))
from database_create_all_funds_long_list import create_table as all_funds_create_table
from database_create_fid_insights_table import create_table as fid_insights_create_table
from database_create_growth_table  import create_table as growth_create_table
from database_create_performance_tables  import create_tables as performance_create_tables
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

DB_HOST = config.DB_HOST
DB_USER = config.DB_USER
DB_PASS = config.DB_PASS
DB_NAME = config.DB_NAME



def run_db_health_check():
    print("\n Starting DB Health Check...\n")

    # 1) Check if MySQL is running
    print("1️⃣ Checking if MySQL service is running...")
    mysql_status = subprocess.run(["systemctl", "is-active", "--quiet", "mariadb"])
    if mysql_status.returncode == 0:
        print("✅ MariaDB/MySQL is running.")
    else:
        print("❌ MariaDB/MySQL is NOT running.")
        return

    # 2) Check DB connection
    print("\nChecking Database Connection connect...")
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        if connection.is_connected():
            print("✅ Connected to database.")
    except Error as e:
        print(f"❌ Failed to connect: {e}")
        return

    # 3) Check tables exist
    print("\nChecking Database Tables…")
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES;")
        existing_tables = {row[0] for row in cursor.fetchall()}
        print(f" {existing_tables }")
    except Error as e:
        print(f"❌ Error while checking tables: {e}")

    # 4) Count rows in each table
    print("\nChecking row counts…")
    try:
        cursor.execute(
            "SELECT table_name, table_rows AS approx_row_count "
            "FROM information_schema.tables "
            "WHERE table_schema = %s "
            "ORDER BY approx_row_count DESC",
            ("investment_db",)
             )
        for table_name, approx_row_count in cursor.fetchall():
            print(f"{table_name:30} {approx_row_count:>15,}")

    except:
            print(f"❌ Could not count rows for tables: {e}")

    # 5) most recent fetch date on Friendly names
    print("\n Checking for more recent updates...")
    cursor.execute("""
        SELECT isin, friendly_name, fetch_date 
          FROM friendly_names
         ORDER BY fetch_date  DESC
         LIMIT 1
    """)
    row = cursor.fetchone()
    if row:
        isin, name, fetch_date  = row
        print(f"Last load: {fetch_date }  →  {isin} / {name}")
    else:
        print("No records in friendly_names.")


    # Cleanup
    cursor.close()
    connection.close()
    print("\nDB Health Check Complete.\n")


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

def check_disk_space():
  # we use shell=True so that the wildcard gets expanded by your shell
    print ("Disk Space in Current use...\n")
    cmd = "du -sh ./* /var/lib/mysql"
    proc = subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True  # so stdout/stderr come back as strings
    )
    if proc.returncode == 0:
        print(proc.stdout)
    else:
        print("Error running disk-usage:", proc.stderr)


print("\n==== Useful Stuff ====")
print("""mysql -u root -e "use investment_db ; show tables;desc fidelity_insights " -p""")
print ("""mysql -u root -e "SELECT    table_name,    table_rows AS approx_row_count  FROM information_schema.tables  WHERE table_schema = 'investment_db'" -p""")
print ("""du -sh ./* /var/lib/mysql""")


if __name__ == "__main__":
    run_db_health_check()
    check_disk_space()


