#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os

# Database connection parameters
DB_HOST = 'localhost'       # Change if your MariaDB server is on a different host
DB_USER = 'root'            # Use your MariaDB username (replace with 'db_user' if created)
DB_PASSWORD = os.getenv('DB_PASSWORD')  # Replace with your MariaDB password
DB_NAME = 'investment_db'    # Database name


def empty_db():
    """
    Wipes all data from the 'all_funds' table.
    """
    try:
        # Connect to the MariaDB database
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Truncate the table (delete all rows)
            truncate_query = "TRUNCATE TABLE all_funds"
            cursor.execute(truncate_query)
            connection.commit()
            print("The all_funds table has been wiped successfully.")

            truncate_query = "TRUNCATE TABLE funds_passed"
            cursor.execute(truncate_query)
            connection.commit()
            print("The funds_passed table has been wiped successfully.")


    except Error as e:
        print("Error while connecting to MariaDB:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MariaDB connection closed.")


def show_all_records(vlimit=99999):
    """
    Retrieves and displays all records from the 'all_funds' table.
    """
    try:
        # Connect to the MariaDB database
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Query to select all records
            select_query = f"SELECT * FROM all_funds limit {vlimit}"
            cursor.execute(select_query)

            # Fetch all rows from the table
            records = cursor.fetchall()

            # Print the records
            if records:
                print("All records in the all_funds table:")
                for row in records:
                    print(row)
            else:
                print("The all_funds table is empty.")

    except Error as e:
        print("Error while connecting to MariaDB:", e)
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MariaDB connection closed.")


def  show_all_sucess(vlimit=99999):
    try:
        # Connect to the MariaDB database
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Query to select all records
            select_query =f"SELECT * FROM funds_passed limit {vlimit}"
            cursor.execute(select_query)

            # Fetch all rows from the table
            records = cursor.fetchall()

            # Print the records
            if records:
                print("All records in the funds passed table:")
                for row in records:
                    print(row)
            else:
                print("The funds passed table is empty.")

    except Error as e:
        print("Error while connecting to MariaDB:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MariaDB connection closed.")



def insert_fund_record_sucess(date, time, fund_name, isin, fee, yield_percentage, frequency, y1_annualized, y3_annualized, y5_annualized, last_years_yield, morning_star_rating):
    """
    Inserts a new record into the funds_passed table.
    """
    try:
        # Establish a connection to the database
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Insert or update query for adding a new record or updating if ISIN exists
            upsert_query = """
            INSERT INTO funds_passed
            (date, time, Fund_Name, ISIN, Fee, Yield, Frequency, Y1_Annualized, Y3_Annualized, Y5_Annualized, Last_Years_Yield, Morning_Star_Rating)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                date = VALUES(date),
                time = VALUES(time),
                Fund_Name = VALUES(Fund_Name),
                Fee = VALUES(Fee),
                Yield = VALUES(Yield),
                Frequency = VALUES(Frequency),
                Y1_Annualized = VALUES(Y1_Annualized),
                Y3_Annualized = VALUES(Y3_Annualized),
                Y5_Annualized = VALUES(Y5_Annualized),
                Last_Years_Yield = VALUES(Last_Years_Yield),
                Morning_Star_Rating = VALUES(Morning_Star_Rating);
            """

            # Data to be inserted or updated
            record = (date, time, fund_name, isin, fee, yield_percentage, frequency, y1_annualized, y3_annualized, y5_annualized, last_years_yield, morning_star_rating)

            # Execute the upsert query with the provided data
            cursor.execute(upsert_query, record)
            connection.commit()
            #print("Record inserted or updated successfully in funds_passed table.")

    except Error as e:
        print("Error while connecting to MariaDB:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def insert_fund_record(date, time, fund, isin, log):
    """
    Inserts a new record into the all_funds table.
    :param date: Date of the record (YYYY-MM-DD)
    :param time: Time of the record (HH:MM:SS)
    :param fund: Name of the fund
    :param isin: ISIN code of the fund
    :param log: Additional log information
    """
    connection = None
    try:
        # Establish a connection to the MariaDB database
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Upsert query to insert a new record or update if ISIN exists
            upsert_query = """
            INSERT INTO all_funds (date, time, fund, isin, log)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                date = VALUES(date),
                time = VALUES(time),
                fund = VALUES(fund),
                log = VALUES(log);
            """

            # Execute the upsert query with the provided data
            cursor.execute(upsert_query, (date, time, fund, isin, log))
            connection.commit()
            print("Record inserted or updated successfully in all_funds table.")

    except Error as e:
        print("Error while connecting to MariaDB:", e)

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
# Example usage


def insert_into_automation(date,time,Feedback):
    connection = None
    try:
        # Establish a connection to the MariaDB database
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Upsert query to insert a new record or update if ISIN exists
            upsert_query = """
            INSERT INTO automation_feedback (date, time, Feedback)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
                date = VALUES(date),
                time = VALUES(time),
                Feedback = VALUES(Feedback);
            """

            # Execute the upsert query with the provided data
            cursor.execute(upsert_query, (date, time, Feedback))
            connection.commit()

    except Error as e:
        print("Error while connecting to MariaDB:", e)

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
# Example usage


def  show_automation():
    try:
        # Connect to the MariaDB database
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Query to select all records
            select_query =f"SELECT * FROM automation_feedback;"
            cursor.execute(select_query)

            # Fetch all rows from the table
            records = cursor.fetchall()

            # Print the records
            if records:
                print("All records in the automation_feedback table:")
                for row in records:
                    print(row)
            else:
                print("The automation_feedback table is empty.")

    except Error as e:
        print("Error while connecting to MariaDB:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MariaDB connection closed.")


if __name__ == "__main__":

    user_input=input("1 for delete all and enter dummy record into fund_success\n2)show all tables data\n3)Insert Dummy record into Automation table\n")

    if user_input=="1":

        user_input=input("I will delete all records and enter 1 new record...")
        # Example data to insert
        empty_db()
        date = datetime.now().date()
        time = datetime.now().time()
        fund = "Example Fund"
        isin = "US1234567890"
        log = "Initial fund record for Example Fund."

        # Insert the record
        insert_fund_record(date, time, fund, isin, log)


        fund_name = "Example Fund"
        isin = "US1234567890"
        fee = 0.75
        yield_percentage = 3.50
        frequency = "Quarterly"
        y1_annualized = 4.20
        y3_annualized = 5.10
        y5_annualized = 6.00
        last_years_yield = 3.80
        morning_star_rating = "4 Stars"

        # Insert the record
        insert_fund_record_sucess(date, time, fund_name, isin, fee, yield_percentage, frequency, y1_annualized, y3_annualized, y5_annualized, last_years_yield, morning_star_rating)
    elif user_input=="2":
        show_all_records()
        show_all_sucess()
        show_automation()
    elif user_input=="3":
        date = datetime.now().date()
        time = datetime.now().time()
        insert_into_automation(date,time,Feedback="3")
    else:
        print("Bad Input")

