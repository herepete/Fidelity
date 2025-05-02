#!/usr/bin/env python3

import os
import subprocess
import sys
from pathlib import Path

# Define helper to run shell commands
def run(cmd, check=True):
    print(f"🔧 Running: {cmd}")
    result = subprocess.run(cmd, shell=True, check=check)
    return result

# Define script directory
SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = SCRIPT_DIR.parent / "config.py"

print("🚀 Starting background setup...")

# System Updates and Package Installation
run("yum update -y")
run("yum install -y python3-pip")
run("pip3 install openai==0.28")
run("pip3 install bs4")
run("pip3 install mysql-connector-python")

run("dnf install -y httpd wget php-fpm php-mysqli php-json php php-devel")

# User Instructions
print("\n📝 Manual Steps Needed:")
print("1. Edit /root/.bashrc and add:\n   export OPENAI_API_KEY=\"your_api_key_here\"")
print(f"2. Edit {CONFIG_PATH} and set the following variables:")
print("   DB_HOST = 'localhost'\n   DB_USER = 'your_username'\n   DB_PASS = 'your_password'")
print(" rather than hard coding my approach is to .bashrc add export DB_PASS='bla' and then change to ")
print("   \n   DB_PASS = os.getenv("DB_PASSWORD")")
input("\n⏸️ Press Enter to continue and start the DB table creation...")

# Install MariaDB
print("📦 Installing MariaDB...")
run("dnf install -y mariadb105-server")

# Start and enable MariaDB
run("systemctl start mariadb")
run("systemctl enable mariadb")

# Secure MariaDB (this is interactive, can’t be fully automated)
print("⚠️ Running MariaDB secure installation — follow the prompts.")
run("mysql_secure_installation", check=False)

# Load config safely
print("📚 Loading config.py")
config = {}
with open(CONFIG_PATH) as f:
    code = compile(f.read(), CONFIG_PATH.name, 'exec')
    exec(code, config)

DB_USER = config.get("DB_USER")
DB_PASS = config.get("DB_PASS")
DB_NAME = config.get("DB_NAME")

if not all([DB_USER, DB_PASS, DB_NAME]):
    sys.exit("❌ DB config values are missing. Check config.py")

# Create Database
print("🛠️ Creating Database...")
run(f'mysql -u "{DB_USER}" -p"{DB_PASS}" -e "CREATE DATABASE IF NOT EXISTS {DB_NAME};"')

# List of scripts to run
scripts = [
    "database_create_all_funds_long_list.py",
    "database_create_fid_insights_table.py",
    "database_create_friendly_names.py",
    "database_create_growth_table.py",
    "database_create_performance_tables.py",
    "database_create_portfolio_tables.py",
    "database_create_risk_and_rating.py",
    "database_dividend_tables.py",
    "database_create_portfolio_tables.py",
]

# Run each Python script
for script in scripts:
    script_path = SCRIPT_DIR / script
    if script_path.exists():
        print(f"\n▶️ Running {script}")
        run(f"python3 {script_path}")
        print("✅ Done")
    else:
        print(f"⚠️ Skipped {script} — not found")

print("\n🎉 Setup complete.")

