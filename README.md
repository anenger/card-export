# card-export

Hello! Welcome to my VCC Card Exporter.  

This is a python3 script. Please run it in python3 or else you will have issues.

# To Run:

Navigate to the folder (probably card-export)

Install the following required dependencies using pip:

pip install -r requirements.txt

Run using python run.py

# Quirks:

If you are exporting stripe:
- If you leave the cardholder blank, it will grab all available cards from the first 100 cardholders and use the info pre-filled on them. This is to make getting the info from generated cards easier.

If you are exporting privacy:
- The script will check against all transactions, this means if there is a card that seems "unused", it may not show up due to previous authorizations or otherwise
