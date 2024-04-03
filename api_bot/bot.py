import requests
import telebot
from telebot.types import ReplyKeyboardRemove, BotCommand

from api_bot.content import Bot
from api_bot.keyboards import make_reply_keyboard
from api_bot.validator import uri_validator, difficulty_validator
from api_bot.status_responses import UserStatus, ProjectStatus, ReviewStatus

from config import settings

token = settings.bot.token
bot = telebot.TeleBot(token=token)

basic_url = settings.bot.basic_url


@bot.message_handler(commands=["start"])
def start_bot(message):
    bot.send_message(message.chat.id, Bot.greeting,
                     reply_markup=make_reply_keyboard("register"))


@bot.message_handler(commands=["register"])
@bot.message_handler(content_types=["text"], func=lambda message: message.text.lower() == "зарегистрироваться")
def start_registering(message):
    bot.send_message(message.chat.id, Bot.ask_password,
                     reply_markup=ReplyKeyboardRemove(), parse_mode="html")

    bot.register_next_step_handler(message, register)


def register(message):
    password = message.text

    user_id = message.from_user.id

    data = {
        "user_id": user_id,
        "password": password
    }

    resp = requests.post(
        url=basic_url + "users/register-user", json=data)

    if resp.status_code == 201:
        bot.send_message(message.chat.id, text=UserStatus.s_201,
                         reply_markup=make_reply_keyboard("send_project"))

    elif resp.status_code == 400:
        bot.send_message(message.chat.id, text=UserStatus.s_400,
                         reply_markup=make_reply_keyboard("send_project"))

    elif resp.status_code == 422:
        bot.send_message(message.chat.id, text=UserStatus.s_422)

        bot.register_next_step_handler(message, register)
        return


@bot.message_handler(commands=["send_project"])
@bot.message_handler(content_types=["text"], func=lambda message: message.text.lower() == "отправить проект")
def get_project_link(message):
    bot.send_message(message.chat.id, Bot.ask_link, parse_mode="html",
                     reply_markup=ReplyKeyboardRemove())

    bot.register_next_step_handler(message, get_project_difficulty)


def get_project_difficulty(message, link=None):

    if not link:
        link = message.text

    is_link = uri_validator(link)
    if not is_link:
        bot.send_message(message.chat.id, ProjectStatus.s_400_error_link)
        get_project_link(message)
        return

    bot.send_message(message.chat.id, Bot.ask_difficulty, parse_mode="html")

    bot.register_next_step_handler(message, ask_about_rules, link)


def ask_about_rules(message, link):
    difficulty = message.text

    is_difficulty = difficulty_validator(difficulty)
    if not is_difficulty:
        bot.send_message(message.chat.id, ProjectStatus.s_422_project_difficulty)
        get_project_difficulty(message, link)
        return

    bot.send_message(message.chat.id, Bot.ask_rules,
                     reply_markup=make_reply_keyboard("not_rules"), parse_mode="html")

    bot.register_next_step_handler(message, send_project, link, difficulty)


def send_project(message, link, difficulty):
    rules = message.text

    user_id = message.from_user.id

    data = {
            "user_id": user_id,
            "project_link": link,
            "project_difficulty": difficulty}

    if rules != "Отправить базовые правила":
        if len(rules) < 30:
            bot.send_message(message.chat.id, ProjectStatus.s_422_review_length,
                             reply_markup=make_reply_keyboard("send_project"))
            bot.register_next_step_handler(message, send_project, link, difficulty)
            return
        
        data["rules"] = str(rules)

    resp = requests.post(
        url=basic_url + "projects/find-pair-or-create-project",
        json=data)

    status = resp.status_code

    if status == 400:
        resp = resp.json()["detail"]["message"]

        if "review" in resp:
            bot.send_message(message.chat.id, ProjectStatus.s_400_error_review,
                             reply_markup=make_reply_keyboard("send_review"))

        elif "github" in resp:
            bot.send_message(message.chat.id, ProjectStatus.s_400_github,
                             reply_markup=make_reply_keyboard("send_project"))
            return

        elif "error" in resp:
            bot.send_message(message.chat.id, ProjectStatus.s_400_error_link,
                             reply_markup=make_reply_keyboard("send_project"))

        else:
            bot.send_message(message.chat.id, ProjectStatus.s_400_error_project,
                             reply_markup=make_reply_keyboard("delete_project"))

    if status == 422:
        if "string_too_short" in resp.json()["detail"][0]["type"]:
            bot.send_message(message.chat.id, ProjectStatus.s_422_review_length,
                             reply_markup=make_reply_keyboard("send_project"))
        else:
            bot.send_message(message.chat.id, ProjectStatus.s_422_project_difficulty,
                             reply_markup=make_reply_keyboard("send_project"))
        return

    if status == 404:
        bot.send_message(message.chat.id, ProjectStatus.s_404_no_project,
                         reply_markup=make_reply_keyboard("send_project"))
        return

    if status == 403:
        bot.send_message(message.chat.id, ProjectStatus.s_403, reply_markup=make_reply_keyboard("register"))

    if status == 201:
        bot.send_message(message.chat.id, ProjectStatus.s_201,
                         reply_markup=make_reply_keyboard("delete_project"))

    if status == 200:
        resp = resp.json()
        user_data_1 = resp["user_data"]
        user_id_1 = user_data_1["user_id"]
        link_1 = user_data_1["project_link"]
        rules_1 = user_data_1["rules"]

        user_data_2 = resp["user for review"]
        user_id_2 = user_data_2["user_id"]
        link_2 = user_data_2["project_link"]
        rules_2 = user_data_2["rules"]

        for user in [user_id_1, user_id_2]:
            bot.send_message(chat_id=user, text=ProjectStatus.s_200,
                             reply_markup=make_reply_keyboard("send_review"), parse_mode="html")

        bot.send_message(chat_id=user_id_1, text="<b>Ссылка </b> на проект, на который необходимо сделать ревью:\n"
                                                 f"{link_2}\n\n"
                                                 f"<b>Критерии</b> для ревью: \n"
                                                 f"{rules_2}", parse_mode="html", disable_web_page_preview=True)

        bot.send_message(chat_id=user_id_2, text=" <b>Ссылка </b> на проект, на который необходимо сделать ревью:\n"
                                                 f"{link_1}\n\n"
                                                 f" <b>Критерии </b> для ревью: \n"
                                                 f"{rules_1}", parse_mode="html")


@bot.message_handler(commands=["delete_project"])
@bot.message_handler(content_types=["text"], func=lambda message: message.text.lower() == "удалить проект")
def delete_project(message):
    user_id = message.from_user.id

    resp = requests.delete(
        url=basic_url + "projects/delete-project",
        params={
            "user_id": user_id
        }
    )

    status = resp.status_code

    if status == 204:
        bot.send_message(message.chat.id, ProjectStatus.s_204,
                         reply_markup=make_reply_keyboard("send_project"))

    if status == 404:
        bot.send_message(message.chat.id, ProjectStatus.s_404_successful_delete,
                         reply_markup=make_reply_keyboard("send_project"))


@bot.message_handler(commands=["send_review"])
@bot.message_handler(content_types=["text"], func=lambda message: message.text.lower() == "отправить ревью")
def get_review(message):
    bot.send_message(message.chat.id, Bot.ask_review, parse_mode="html")
    bot.register_next_step_handler(message, send_review)


def send_review(message):
    review = message.text
    user_id = message.from_user.id

    data = {
            "user_id": user_id,
            "review_text": review
    }

    resp = requests.post(
        url=basic_url + "reviews/send-review",
        json=data)

    status = resp.status_code

    if status == 403:
        bot.send_message(message.chat.id, ReviewStatus.s_403, reply_markup=make_reply_keyboard("register"))

    if status == 404:
        resp = resp.json()["detail"]["message"]

        if "pair" in resp:
            bot.send_message(message.chat.id, ReviewStatus.s_404_no_pair,
                             reply_markup=make_reply_keyboard("delete_project"))

        elif "project" in resp:
            bot.send_message(message.chat.id, ReviewStatus.s_404_no_project,
                             reply_markup=make_reply_keyboard("send_project"))

    if status == 422:
        bot.send_message(message.chat.id, ReviewStatus.s_422)
        get_review(message)
        return

    if status == 201:
        bot.send_message(message.chat.id, ReviewStatus.s_201, reply_markup=make_reply_keyboard("delete_review"))

    if status == 200:
        resp = resp.json()["reviews"]
        user_id_1 = resp["user_id_1"]
        review_1 = resp["review_for_1"]

        user_id_2 = resp["user_id_2"]
        review_2 = resp["review_for_2"]

        for user in [user_id_1, user_id_2]:
            bot.send_message(chat_id=user, text=ReviewStatus.s_200,
                             reply_markup=make_reply_keyboard("send_project"), parse_mode="html")

        bot.send_message(chat_id=user_id_1, text=review_1)
        bot.send_message(chat_id=user_id_2, text=review_2)


@bot.message_handler(commands=["delete_review"])
def delete_review(message):
    user_id = message.from_user.id

    resp = requests.delete(
        url=basic_url + "reviews/delete-review",
        params={
            "user_id": user_id
        }
    )

    status = resp.status_code

    if status == 204:
        bot.send_message(message.chat.id, ReviewStatus.s_204,
                         reply_markup=make_reply_keyboard("send_review"))

    if status == 404:
        bot.send_message(message.chat.id, ReviewStatus.s_404_no_pair)


commands = [
        BotCommand('start', 'запуск бота'),
        BotCommand('register', 'зарегистрироваться'),
        BotCommand('send_project', 'отправить проект'),
        BotCommand('delete_project', 'удалить проект'),
        BotCommand('send_review ', 'отправить ревью'),
        BotCommand('delete_review', 'удалить ревью')
    ]


def run_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    bot.set_my_commands(commands)

    bot.infinity_polling()
