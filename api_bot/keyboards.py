from telebot.types import ReplyKeyboardMarkup


def make_reply_keyboard(arg):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    if arg == "register":
        keyboard.add("Зарегистрироваться")

    elif arg == "send_project":
        keyboard.add("Отправить проект")

    elif arg == "delete_project":
        keyboard.add("Удалить проект")

    elif arg == "send_review":
        keyboard.add("Отправить ревью")

    elif arg == "delete_review":
        keyboard.add("Удалить ревью")

    elif arg == "not_rules":
        keyboard.add("Отправить базовые правила")

    return keyboard