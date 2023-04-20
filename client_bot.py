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

MEETUP_TEXT = "Приветствую в чат боте сервиса по аренде складкского помещения для вещей."

EXAMPLES_INTRO_TEXT = "Ниже перечислены основные примеры испоьзования:"

EXAMPLES_OS_USE = [
    "Вы можете положить свой старый хлам, который жалко выбрасывать.",
    "Вы можете складировать достаточно объёмные сезонные предметы: велосипед, снегоуборочную машину и т.д.",
]

RULES_INTRO_TEXT = "Для склада существует ряд правил:"

RULES = [
    "Не использовать склад в злоумышленных целях",
    "Не обманывать работников склада в целях скрытно положить на хранение запрещённый предмет",
]

UNALLOWED_ITEMS = [
    "Жидкости",
    "Органические продукты",
    "Животных",
    "Химические реагенты",
    "Облучённые чрезмерной дозой радиации предметы",
    "Все прочие запрещённые для хранения предметы по УК РФ",
]

ALLOWED_ITEMS = [
    "Книги",
    "Бытовую технику",
    "Спортивный инвентарь",
    "Одежду",
    "Предметы роскоши",
]


def get_intro_message_text() -> str:
    return MEETUP_TEXT + "\n" + EXAMPLES_INTRO_TEXT + "\n" + "\n".join(EXAMPLES_OS_USE)


def get_rules_messages_texts() -> tuple[str, str, str]:
    main_rules = RULES_INTRO_TEXT + "\n" + "\n".join(RULES)
    allowed_items = "Разрешено сдавать на хранение:" + "\n" + "\n".join(ALLOWED_ITEMS)
    unallowed_items = "Запрещено сдавать на хранение:" + "\n" + "\n".join(UNALLOWED_ITEMS)
    return main_rules, allowed_items, unallowed_items


@bot.message_handler(commands=['start'])
def bot_start(message):
    access = None
    if access:
        bot.send_message(
            message.chat.id,
            "Авторизованный пользватель.",
            reply_markup=make_keyboard(),
        )
    else:  # пользователя нет в БД
        messsage_text = get_intro_message_text()
        bot.send_message(
            message.chat.id,
            messsage_text,
            reply_markup=make_keyboard(),
        )


def make_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('Правила'))
    return keyboard


@bot.message_handler(func=lambda message: message.text == 'Правила')
def pay_for_subscription(message):
    rules = get_rules_message_text()
    for rule in rules:
        bot.send_message(
            message.chat.id,
            rule,
            reply_markup=make_keyboard(),
        )


def main():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as error:
            print(error)
            time.sleep(5)


if __name__ == '__main__':
    main()
