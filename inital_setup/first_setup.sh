#!/bin/bash
# run as root
echo "Starting on installing some background bits"
yum update
yum install pip
pip3.9 install openai==0.28
pip3.9 install bs4 
pip3.9 install mysql-connector-python
dnf install -y httpd wget php-fpm php-mysqli php-json php php-devel # not sure if is needed?

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Next steps for you"
echo "To /root/.bashrc add (this can be done after the DB install)..."
echo "    -export OPENAI_API_KEY="bla""
echo "To ../config.py add (This needs to be done before the script can continue)..."
echo "    - DB_HOST='localhost'"
echo "    - DB_USER='bla'"
echo "    - DB_PASSWORD='bla'"
echo "⏸️ Press Enter to continue and start the DB table creation..."
read

echo "Starting mysql install..."
dnf install mariadb105-server

# Start MariaDB service
echo "Starting MariaDB service..."
sudo systemctl start mariadb

echo "Starting MariaDB and Starting it on boot..."
# Enable MariaDB to start on boot
sudo systemctl enable mariadb

# Secure MariaDB Installation (you might need to customize this section for interactive configuration)
echo "Securing MariaDB Installation..."
sudo mysql_secure_installation


# Get the directory of the current script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Load config from parent directory
source "$SCRIPT_DIR/../config.sh"

echo "Creating Database..."
# Create the database
mysql -u "$DB_USER" -p"$DB_PASS" -e "CREATE DATABASE IF NOT EXISTS \`$DB_NAME\`;"


echo "Creating Database tables..."
# List of Python files to run (adjust names as needed)
FILES=(
    "database_create_all_funds_long_list.py"
    "database_create_fid_insights_table.py"
    "database_create_friendly_names.py"
    "database_create_growth_table.py"
    "database_create_performance_tables.py"
    "database_create_portfolio_tables.py"
    "database_create_risk_and_rating.py"
    "database_dividend_tables.py"
    "database_create_portfolio_tables.py"
)

# Run each Python file
for file in "${FILES[@]}"; do
    echo "▶️ Running $file"
    python3 "$SCRIPT_DIR/$file"
    echo "✅ Finished $file"
    echo "-----------------------------"
done




echo "Troubleshooting script bla"

