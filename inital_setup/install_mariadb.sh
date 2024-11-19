#!/bin/bash

# Update package information
dnf upgrade -y
dnf install -y httpd wget php-fpm php-mysqli php-json php php-devel
dnf install mariadb105-server

# Start MariaDB service
echo "Starting MariaDB service..."
sudo systemctl start mariadb

# Enable MariaDB to start on boot
sudo systemctl enable mariadb

# Secure MariaDB Installation (you might need to customize this section for interactive configuration)
echo "Securing MariaDB Installation..."
sudo mysql_secure_installation

# MariaDB root password
MARIADB_ROOT_PASSWORD=$DB_PASSWORD  # Set your root password here

# Create MariaDB commands to set up the database and table
MARIADB_COMMANDS="
CREATE DATABASE IF NOT EXISTS investment_db;
USE investment_db;
CREATE TABLE IF NOT EXISTS all_funds (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    time TIME,
    fund VARCHAR(255),
    isin VARCHAR(255),
    log TEXT
);
"
# SQL query to create the table
create_table_query="USE investment_db;
CREATE TABLE IF NOT EXISTS funds_passed (
	Id INT AUTO_INCREMENT PRIMARY KEY,
        date DATE,
        time TIME,
        Fund_Name VARCHAR(255),
        ISIN VARCHAR(20),
        Fee DECIMAL(5, 2),
        Yield DECIMAL(5, 2),
        Frequency VARCHAR(50),
        Y1_Annualized DECIMAL(5, 2),
        Y3_Annualized DECIMAL(5, 2),
        Y5_Annualized DECIMAL(5, 2),
        Last_Years_Yield DECIMAL(5, 2),
        Morning_Star_Rating VARCHAR(50)
);
"


create_automation_feedback="USE investment_db;
CREATE TABLE IF NOT EXISTS automation_feedback 
	( Id INT AUTO_INCREMENT PRIMARY KEY,
        date DATE,
        time TIME,
	Feedback VARCHAR(2255)
);
"

# Execute MariaDB commands

pip install mysql-connector-python

echo "Creating database and table..."
mysql -u root -p"$MARIADB_ROOT_PASSWORD" -e "$MARIADB_COMMANDS"
mysql -u root -p"$MARIADB_ROOT_PASSWORD" -e "$create_table_query"
mysql -u root -p"$MARIADB_ROOT_PASSWORD" -e "$create_automation_feedback"


#echo "Sorting out Permissions..."
#mysql -u root -p"$MARIADB_ROOT_PASSWORD" -e "CREATE USER 'db_user'@'localhost' IDENTIFIED BY 'db_user_password';GRANT ALL PRIVILEGES ON investment_db.* TO 'db_user'@'localhost';FLUSH PRIVILEGES;"


echo "MariaDB installation and table setup complete."

