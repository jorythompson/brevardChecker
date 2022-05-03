Brevard County Property Appraiser Checker
===========================
This script validates data from a spreadsheet with the property appraiser's website.  In the event there are any differences, it will alert the user via email and update the spreadsheet if desired.

## Installation
You will need Python 3.6 installed or higher to run this app.  

You can install it with the following command:
```bash
pip3 install -r requirements.txt
```

Once installed, run it once to create the configuration file and spreadsheet:
```bash
python3 main.py --config YOUR_CONFIG_FILE
```

This will create the specified configuration file and the default spreadsheet (brevard_data.xls).

Edit the configuration file with your own information.  If you prefer a different spreadsheet name, you can change it in the configuration file and either rename the default one, or run the script again to create a new one.

The spreadsheet has the following format:

| #   | Account | Owner | Mailing Address | Site Address |
|-----|---------|-------|-----------------|--------------|
| 1   |
| 2   |
| 3   |

Fill in the unique Brevard County account number on each row in the "Account" column. 

If "auto-update spreadsheet" in the configuration file is set to True, running the application once will update the fields in the other columns.

If "auto-update spreadsheet" is True, as you add more accounts and the script is run again, the spreadsheet will be updated with the new information.  If email is turned on.  
Note that if the account information is blank, the user will not be notified even if "send messages" is set to True.

The configuration file has the following format:
```
[web]
page delay = 1

[debug]
debug = True
debug folder = debug

[spreadsheet]
spreadsheet file name = brevard_data.xlsx
auto-update spreadsheet = True

[files]
json extension = bs4
log config file = logging.ini

[email connection]
username = email-account-username
password = email-account-password
from = email-from-address
smtp_host = smtp.gmail.com
smtp_port = 587
send messages = False
email_recipients = comma-delimited-list-of-email-addresses
```