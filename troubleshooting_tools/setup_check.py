#!/usr/bin/python3.9
import os
import requests
import subprocess
import socket
import sys
import test_openai

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import config  # after sys.path.append




def project_status():


    try:
        if  config.testing ==1:
            mode="Testing"
        elif config.testing ==0:
            mode="Live"
        else:
            mode="Unsure"
    except:
        mode="Unsure -Something Went Wrong"

    try:
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            ip_data = response.json()
            web_address = "http://" + ip_data['ip']
        else:
            web_address = "Could not get Ip Address"
    except Exception as e:
            web_address = "Could not get Ip Address"

    try:
        # Check the status of the MariaDB service
        result = subprocess.run(
            ["systemctl", "is-active", "--quiet", "mariadb"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # If the command exits with code 0, MariaDB is running
        maria_running="Yes"
    except Exception as e:
        maria_running="No"

    flask_running = False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(("127.0.0.1", 5000))
            flask_running = "Yes"
        except OSError:
            flask_running = "No"


    apache_running = False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(("127.0.0.1", 80))
            apache_running = "Yes"
        except OSError:
            apache_running = "No"
    try:
        rv=test_openai.return_test_query()
        if rv == 1:
            openai_running="Running"
        else:
            openai_running="Not Running"
    except:
            openai_running="Not Running-Something Errored"
    try:
        db_password = os.getenv("DB_PASSWORD")
        if db_password:
            db_password_set="Yes"
        else:
            db_password_set="No"
    except:
            db_password_set="No-Something Errored"

    try:
        db_password = os.getenv("OPENAI_API_KEY")
        if db_password:
            openai_key_set="Yes"
        else:
            openai_key_set="No"
    except:
            openai_key_set="No-Something Errored"

    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BLUE = "\033[94m"

    def color_bool(value):
        return f"{GREEN}Yes{RESET}" if value == "Yes" else f"{RED}No{RESET}"

    print(f"{BOLD}{BLUE}==== Project Status ===={RESET}")
    print(f"{CYAN}Mode: {YELLOW}{mode}{RESET}")
    print(f"MariaDB Running: {color_bool(maria_running)}")
    print(f"Flask Running: {color_bool(flask_running)}")
    print(f"Apache Running: {color_bool(apache_running)}")
    print(f"OpenAI Connection Working: {YELLOW}{openai_running}{RESET}")
    print(f"Env - DB Password Set: {color_bool(db_password_set)}")
    print(f"Env - OpenAI Key Found: {color_bool(openai_key_set)}")
    print(f"{CYAN}Web Address: {GREEN}{web_address}{RESET}")
    print(f"{BLUE}=========================={RESET}")




if __name__ == "__main__":
    project_status()

