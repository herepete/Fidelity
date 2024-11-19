#!/usr/bin/python3
from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error
from datetime import timedelta
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Database connection parameters
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD =  os.getenv('DB_PASSWORD')  # Replace with your root password
DB_NAME = 'investment_db'            # Replace with your database name

def get_db_connection():
    """Establishes and returns a connection to the database."""
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def serialize_data(data):
    """Converts non-serializable fields (like timedelta) to strings."""
    serialized_data = []
    for row in data:
        serialized_row = []
        for value in row:
            # Check if the value is a timedelta and convert to string if so
            if isinstance(value, timedelta):
                serialized_row.append(str(value))
            else:
                serialized_row.append(value)
        serialized_data.append(serialized_row)
    return serialized_data

@app.route('/api/all_funds', methods=['GET'])
def get_all_funds():
    """API endpoint to retrieve all records from the all_funds table."""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM all_funds")
        funds = cursor.fetchall()
        return jsonify(serialize_data(funds))  # Serialize data before returning
    except Error as e:
        return jsonify({"error": str(e)})
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/api/funds_passed', methods=['GET'])
def get_funds_passed():
    """API endpoint to retrieve all records from the funds_passed table."""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM funds_passed")
        funds = cursor.fetchall()
        return jsonify(serialize_data(funds))  # Serialize data before returning
    except Error as e:
        return jsonify({"error": str(e)})
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/api/automation_feedback', methods=['GET'])
def get_ai_feedback():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT *  FROM automation_feedback")
        feedback_data = cursor.fetchall()
        
        # Format the data as a list of dictionaries
        return jsonify(serialize_data(feedback_data))  # Serialize data before returning
    except Error as e:
        return jsonify({"error": str(e)})
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

