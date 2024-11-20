#!/bin/bash
yum update
#yum install git
#git clone https://github.com/herepete/Fidelity.git
yum install pip
pip3.9 install bs4 pandas
pip3.9 install openai==0.28
pip3.9 install flask-cors
cp flaskapp.service /etc/systemd/system/flaskapp.service

echo "i have installed what i can..."
echo "Next steps for you"
echo "To /root/.bashrc add..."
echo "    -export OPENAI_API_KEY="bla""
echo "    -export DB_HOST='localhost'"
echo "    -export DB_USER='bla'"
echo "    -export DB_PASSWORD='bla'"
echo "Then run the install_flask.py & install_mariadb.sh scripts "
echo "Restart appache"

echo "Then run main.py \n\t check the value of the pre-checks & fix anything outstanding\n\tYou will need to start Flask"


