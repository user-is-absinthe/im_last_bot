import telegram.ext as t
import logging


PATH_TO_LOG = '/Users/owl/Pycharm/PycharmProjects/im_last_bot/tiny_client/tests/files/test.log'
OVERWRITE_LOG = True
PATH_TO_TOKEN = '/Users/owl/Pycharm/PycharmProjects/im_last_bot/tiny_client/bot_token.txt'


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)s] [%(funcName)s] [%(levelname)s]  %(message)s",
    handlers=[
        logging.FileHandler(PATH_TO_LOG),
        logging.StreamHandler()
    ])

token_file = open(PATH_TO_TOKEN, 'r')
TOKEN = token_file.read()

# REQUEST_KWARGS = {
#     'proxy_url': 'http://ip:port/',
#     # Optional, if you need authentication:
#     'username': 'user',
#     'password': 'pass',
# }

REQUEST_KWARGS = {
    'proxy_url': 'socks5h://ip:port',
    # Optional, if you need authentication:
    'urllib3_proxy_kwargs': {
        'username': 'user',
        'password': 'pass',
    },
    # 'rdns': True
}

updater = t.Updater(TOKEN, request_kwargs=REQUEST_KWARGS)
my_dcp = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


start_handler = t.CommandHandler('start', start)
my_dcp.add_handler(start_handler)

updater.start_polling()
