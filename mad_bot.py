import io
import json
from google.cloud import language
from google.oauth2 import service_account
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import analysis
import logging

client = ''

def analyze(bot, update, args):
    global client
    message = ' '.join(args)
    score = analysis.analyze(message, client).score
    message = "Your message of '" + message + "' yielded a score of: " + str(score)
    bot.send_message(chat_id=update.message.chat_id, text=message)

def main():
    with open('botkey.txt', 'r') as bot_key:
        key = bot_key.read().rstrip()
        updater = Updater(key)

    with open('apikey.json', 'r') as key_file:
        key = key_file.read()
        key_json = json.loads(key, strict=False)
        creds = service_account.Credentials.from_service_account_info(key_json)
    
    global client
    client = language.LanguageServiceClient(credentials=creds)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    updater.dispatcher.add_handler(CommandHandler('analyze', analyze, pass_args=True))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
