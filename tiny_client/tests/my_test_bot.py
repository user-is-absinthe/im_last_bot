from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram import InlineQueryResultArticle
from telegram import InputTextMessageContent
from telegram.ext import InlineQueryHandler
import logging


PATH_TO_TOKEN = 'bot_token.txt'
PATH_TO_LOG = 'test_log.log'
OVERWRITE_LOG = 0


token_file = open(PATH_TO_TOKEN, 'r')
token = token_file.read()

updater = Updater(token=token)
dispatcher = updater.dispatcher

if OVERWRITE_LOG:
    logging.basicConfig(filename='PATH_TO_LOG', level=logging.INFO, filemode="w")
else:
    logging.basicConfig(filename='PATH_TO_LOG', level=logging.INFO)


def to_log(message, level=-1):
    # level = DEBUG (not saving in file), INFO, WARNING, ERROR, CRITICAL
    if level == 'DEBUG':
        logging.debug(message)
    elif level == 'INFO':
        logging.info(message)
    # elif level == 'WARNING':
    #     logging.warning(message)
    else:
        logging.error(message)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="First message.")


def echo(bot, update, answered='Sorry.'):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
    print(update)
    # bot.send_message(chat_id=update.message.chat_id, text=answered)


if __name__ == '__main__':
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    updater.start_polling()

    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)
