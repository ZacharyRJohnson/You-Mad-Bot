# You-Mad-Bot
Telegram bot which uses Google Cloud's Natural Language API to determine if a message was glad or mad. Built using Python 3 and the 'python-telegram-bot' api wrapper for Python. The bot reads and stores each messages that is sent in the group chat it is in and analyzes and store the message in a group chat map.

# Setup
You must get your own google cloud platform service account key and telegram bot key.
To run the bot, you must clone the repository and make sure you have python3, pip, and virtualenv installed. To install virtualenv on Ubuntu type
```
sudo pip install virtual env
```
Then inside of the cloned repository run
```
source env/bin/activate
```
This puts you inside of the virtual enviornment that has the packages installed to run the bot. From there you must have your telegram bot key in a file called *botkey.txt* and the gcp api key in *apikey.json*. Once you have those keys in the bots repository you can run the bot with
```
python3 mad_bot.py
```
When you want to stop the bot just put command 'C', ^C, into the terminal and to exit the virtualenv type
```
deactivate
```
