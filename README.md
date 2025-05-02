everything written up in:  <br>
<br>
Assumption setup up in an AWS VM with Amazon linux as the OS
<br>
Steps:
<br>
1) you will need to install Git 
<br>
2) Download repo git clone https://github.com/herepete/Fidelity.git
<br>
3) run ./inital_setup/first_setup.sh - follow the password prompts as stuff can get a bit funky
<br>
4) run ./get_fidelity_data/populate_database_tables.py -t
<br>
5) run ./database_operations/database_health_check.py  
<br>
