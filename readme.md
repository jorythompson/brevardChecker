Brevard County Property Appraiser Checker
===========================
# General Information
This script validates data from a spreadsheet with the property appraiser's website.
It looks up the accounts specified in a spreadsheet and compares the results to the values stored in the spreadsheet. 
In the event there are any differences, it can alert the user via email and update the spreadsheet if desired.
The intent is for this to be run periodically, but it can be run manually as well.

# Need
There are numerous accounts of people having their properties usurped by bad actors throughout the country.
There are several steps to this process and the last is where the property is put into another person's name and sold to an unsuspecting buyer.
Once the middleman has made their money, they can completely disappear, leaving the property in the hands of the buyer and the real owner no recourse.
This script will help you find these accounts and alert you if they are identified.

# Installation
You will need Python 3.6 installed or higher to run this app.
You may need to install the rust compiler:
```bash
sudo apt-get install rust
```
## Virtual Environment
If you are not using a virtual environment, you can skip this step.
### Install the virtual environment 
If decide to run this script in a virtual environment, you must create one first:
```bash
virtualenv -p python3 venv
```
### Activate the virtual environment
Then you can activate it:
```bash
source venv/bin/activate.sh
```
## Install the library dependencies
Whether you use a virtual environment or not, you must install the libraries from the requirements.txt file.
You can install them with the following command:
(Note that you may need to install rust to build the selenium driver)
```bash
pip3 install -r requirements.txt
```

# Running the script
Once installed, run it once to create the configuration file and spreadsheet:
It is intended to be run periodically (in a Unix cron or Windows service, but you can run it manually as well.
```bash
python3 brevardChecker.py --config YOUR_CONFIG_FILE
```
This will create the specified configuration file and the default spreadsheet (brevard_data.xls).
# Configuration
The configuration file will automatically be generated if it does not exist. 
You can edit the file to change the default values. 
The configuration file has the following structure:
## [web]
### page delay
integer: This is the number of seconds to wait between each page load.  
This is to prevent the script from capturing the data prematurely.
## [debug]
### debug
boolean: Indicates the downloaded soap json should be used if it exists, or downloaded and used. 

***NOTE: IF THIS IS SET TO TRUE, THE DATA WILL NOT BE CURRENT!!!!*** 
### debug folder
string: The folder where the downloaded json soam files from the website are stored (one for each property) if debug is set to True.
## [spreadsheet]
### spreadsheet file name
string: The name of the spreadsheet file.
This is the name of the spreadsheet file that will be created.
The default is brevard_data.xls.
### auto-update spreadsheet
boolean: Indicates whether the spreadsheet should be updated if there are any differences.
The default is false.
## [files]
### json extension
string: The extension of the json files.  The default is .json.
### log config file
string: The name of the log config file.  The default is logging.config.
## [email connection]
### username
string: The username for the email connection.
### password
string: The password for the email connection.
### from
string: The email address that the email will be sent from.
### smtp_host
integer: The smtp host for the email connection.
### smtp_port
integer: The smtp port for the email connection.
### send messages
boolean: Indicates whether the script should send messages via email.
The default is false.
### email recipients
string: The email recipients.
This is a comma separated list of email addresses.

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
email recipients = comma-delimited-list-of-email-addresses
```

# Spreadsheet
Edit the configuration file with your own settings.
If you prefer a different spreadsheet name, you can change it in the configuration file and either rename the default one, or run the script again to create a new one.
The spreadsheet has the following format:

| #   | Account | Owner | Mailing Address | Site Address | Notes |
|-----|---------|-------|-----------------|--------------|-------|
| 1   |
| 2   |
| 3   |

Fill in the unique Brevard County account number on each row in the "Account" column.
***NOTE: blank cells in the "Account" column will cause the script to stop processing***

The "Notes" column is for you to add any notes for a particular property.
It is only used for reporting.

If "auto-update spreadsheet" in the configuration file is set to True, running the application will update the fields in the other columns.

If "auto-update spreadsheet" is True, as you add more accounts and the script is run again, the spreadsheet will be updated with the new information.
If email is turned on.  
Note that if the account information is blank, the user will not be notified even if "send messages" is set to True.
