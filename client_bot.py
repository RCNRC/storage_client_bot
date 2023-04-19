import sys
import logging
import time
import signal
import telebot
from environs import Env


logging.basicConfig(filename='bot.log', level=logging.INFO)


env = Env()
env.read_env(override=True)
bot = telebot.TeleBot(env.str("TELEGRAM_CLIENTS_BOT_API_TOKEN"))


def signal_handler(signum, frame):
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


CURRENT_ORDER_ID = 0


def main():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as error:
            print(error)
            time.sleep(5)


if __name__ == '__main__':
    main()
