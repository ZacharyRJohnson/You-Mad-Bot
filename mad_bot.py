import io
import json
import collections
import random
from google.cloud import language
from google.oauth2 import service_account
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import analysis
import logging

client = ''

# Holds a dictionary for each group which holds messages from each user in that group
groups = {}

def analyze(bot, update, args):
    """
        Analyzes the sentiment of a single inputed message or the last 10 messages
        of the user which called this function. By inputing 'me' a user can see
        what their average sentiment score is over their last 10 messages.
    """
    global client
    message = ' '.join(args)
    if(len(message.split()) == 1 and message.lower() == 'me'):
        user = update.message.from_user
        user_id = user.id
        chat_id = update.message.chat_id
        if chat_id in groups.keys():
            cur_group = groups[chat_id]
            if user_id in cur_group.keys():
                messages = cur_group[user_id]
                sentiment = analysis.get_average_sentiment(messages, client)
                avg_score = "%.4f" % sentiment.avg_score
                message = "{} has had an average sentiment score of {} for their last 10 messages"\
                                .format(user.first_name, avg_score)
                bot.send_message(chat_id=update.message.chat_id, text=message)
            else:
                message = "I don't have any messages stored from {} yet"\
                                .format(user.first_name)
                bot.send_message(chat_id=update.message.chat_id, text=message)
        else:
            message = "I don't have any messages stored from this chat yet"
            bot.send_message(chat_id=update.message.chat_id, text=message)
    else:
        score = "%.4f" % analysis.analyze(message, client).score
        message = "Your message of '" + message + "' yielded a score of: " + score
        bot.send_message(chat_id=update.message.chat_id, text=message)

def score_board(bot, update):
    """
        Posts a score board showing the average sentiment scores of all members
        in decreasing order. Only posts scores of members that the bot has stored
        while it has been up.
    """
    global client
    chat_id = update.message.chat_id
    if chat_id not in groups.keys():
        message = "I don't have any messages stored from that group yet."
        bot.send_message(chat_id=chat_id, text=message)
        return
    cur_group = groups[chat_id]
    board = []
    for user_id in cur_group.keys():
        name = bot.get_chat_member(chat_id, user_id).user.first_name
        avg_score = analysis.get_average_sentiment(cur_group[user_id], client).avg_score
        board.append((name, "%.4f" % avg_score))
    board.sort(key=lambda x: x[1])
    message = "<pre>-- Sentiment Score Board --\n"
    message += "{:^17} {:^8}".format("Chat Member", "Score") + "\n"
    for member in board:
        if(float(member[1]) >= 0):
            message += "{:^13} {:>10}".format(member[0], " " + member[1]) + "\n"
        else:
            message += "{:^13} {:>10}".format(member[0], member[1]) + "\n"
    message += "</pre>"
    print(message)
    bot.send_message(chat_id = chat_id, parse_mode="HTML", text=message)

def respond_analysis(bot, update):
    """
        Listens to each message posted in the chat and if it is above or below
        a given threshold the bot will send a message directed at the user that
        sent the positive or negative message. Also stores each message it recieves
        in the groups hashmap. It makes a map for each group chat that contains
        each user and their 10 most recent messages.
    """
    global client, groups
    message = update.message
    text = message.text
    print(text)
    score = analysis.analyze(text, client).score
    if(score >= .5):
        score = "%.4f" % score
        bot_msg = "Whoa {} you are looking pretty happy there with a sentiment score of: {}" \
                    .format(message.from_user.first_name, str(score))
        bot.send_message(chat_id=message.chat_id, text=bot_msg)
    elif(score <= -.5):
        score = "%.3f" % score
        bot_msg = "You gotta calm down {}, you're super mad right now with a sentiment score of : {}" \
                    .format(message.from_user.first_name, str(score))
        bot.send_message(chat_id=message.chat_id, text=bot_msg)
    elif(score == 0.0):
        bot_msg = "I either can't analyze your message or you are extremely neutral {}" \
                    .format(message.from_user.first_name)
        bot.send_message(chat_id=message.chat_id, text=bot_msg)
    
    chat_id = message.chat_id
    user_id = message.from_user.id
    
    if chat_id in groups.keys():
        cur_group = groups[chat_id]
    else:
        groups[chat_id] = {}
        cur_group = groups[chat_id]
    
    if user_id in cur_group.keys():
        messages = cur_group[user_id]
    else:
        cur_group[user_id] = collections.deque(maxlen=10)
        messages = cur_group[user_id]
    messages.append(text)

def test_messages(bot, update):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    print(groups)
    print(groups[chat_id])
    print(groups[chat_id][user_id])
    print(groups[chat_id][user_id][0])

def main():
    
    # Bot key for the telegram bot
    with open('botkey.txt', 'r') as bot_key:
        key = bot_key.read().rstrip()
        updater = Updater(key)
    
    # API key for the google cloud platform calls
    with open('apikey.json', 'r') as key_file:
        key = key_file.read()
        key_json = json.loads(key, strict=False)
        creds = service_account.Credentials.from_service_account_info(key_json)
    
    global client
    client = language.LanguageServiceClient(credentials=creds)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    updater.dispatcher.add_handler(CommandHandler('analyze', analyze, pass_args=True))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, respond_analysis))
    updater.dispatcher.add_handler(CommandHandler('test', test_messages))
    updater.dispatcher.add_handler(CommandHandler('scoreBoard', score_board))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
