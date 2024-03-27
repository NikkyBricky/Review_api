import requests
import telebot
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, BotCommand, BotCommandScope
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")
bot = telebot.TeleBot(token=token)

basic_url = "http://158.160.138.75/api/v1/"


def make_reply_keyboard(args):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for arg in args:
        keyboard.add(arg)

    return keyboard


register_keyboard = make_reply_keyboard(["Зарегистрироваться"])
send_project_keyboard = make_reply_keyboard(["Отправить проект"])
delete_project_keyboard = make_reply_keyboard(["Удалить проект"])
send_review_keyboard = make_reply_keyboard(["Отправить ревью"])
delete_review_keyboard = make_reply_keyboard(["Удалить ревью"])


@bot.message_handler(commands=["start"])
def start_bot(message):
    commands = [  # Установка списка команд с областью видимости и описанием
        BotCommand('start', 'запуск бота'),
        BotCommand('register', 'зарегистрироваться'),
        BotCommand('send_project', 'отправить проект'),
        BotCommand('delete_project', 'удалить проект'),
        BotCommand('send_review ', 'отправить ревью'),
        BotCommand('delete_review', 'удалить ревью')
    ]

    bot.set_my_commands(commands)
    BotCommandScope('private', chat_id=message.chat.id)

    bot.send_message(message.chat.id, "Привет! Я бот, который предоставит вам возможность писать ревью на проекты"
                                      "других людей и получать ревью на ваши. Для начала вам нужно зарегистрироваться.",
                     reply_markup=register_keyboard)


@bot.message_handler(commands=["register"])
@bot.message_handler(content_types=["text"], func=lambda message: message.text.lower() == "зарегистрироваться🔐")
def start_registering(message):
    bot.send_message(message.chat.id, "Придумайте пароль <b>(не менее 8 символов)</b>:",
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

    if resp.status_code in [200, 201]:
        bot.send_message(message.chat.id, text="Вы успешно добавлены в базу данных!",
                         reply_markup=send_project_keyboard)

    elif resp.status_code == 400:
        bot.send_message(message.chat.id, text="Такой пользователь уже существует.", reply_markup=send_project_keyboard)

    elif resp.status_code == 422:
        bot.send_message(message.chat.id, text="Пароль слишком короткий, попробуйте еще раз.")

        bot.register_next_step_handler(message, register)
        return


@bot.message_handler(commands=["send_project"])
@bot.message_handler(content_types=["text"], func=lambda message: message.text.lower() == "отправить проект")
def get_project_link(message):
    bot.send_message(message.chat.id, "Отправьте  <b>ссылку на github </b> проекта:", parse_mode="html",
                     reply_markup=ReplyKeyboardRemove())

    bot.register_next_step_handler(message, get_project_difficulty)


def get_project_difficulty(message):
    link = message.text

    bot.send_message(message.chat.id, "Оцените сложность своего проекта от 1 до 10:\n\n"
                                      "Расчет сложности <b>(начиная с 1 балла)</b> "
                                      "производится по следующим параметрам:\n\n"
                                      "1. В одном из файлов проекта более 300 строк кода "
                                      "(текстовые файлы не считаются). <b>(+2 балла)</b>\n\n"
                                      "2. В проекте использованы малоизвестные/новые библиотеки и модули. "
                                      "<b>(+1 балл)</b>\n\n"
                                      "3. В проекте не менее 3 файлов кода, "
                                      "в каждом из которых не менее 100 строк кода"
                                      " (README, requirements и .env не считаются).  <b>(+2 балла)</b>\n\n"
                                      "4. Код проекта сложно читать, "
                                      "названия переменных и функций не соответствуют"
                                      " их назначению. <b>(+1 балл)</b>\n\n"
                                      "5. Отсутствует документация к проекту.  <b>(+1 балл)</b>\n\n"
                                      "6. Отсутствует модульность проекта. "
                                      "Все элементы, относящиеся к разным задачам,"
                                      " собраны в одном файле.  <b>(+2 балла)</b>\n\n", parse_mode="html")

    bot.register_next_step_handler(message, ask_about_rules, link)


def ask_about_rules(message, link):
    difficulty = message.text

    bot.send_message(message.chat.id, "Если хотите отправить критерии к проекту, то можете это сделать прямо"
                                      "сейчас. Если нет (отправьте 1), то будут отправлены базовые критерии:\n\n"
                                      "1. Код хорошо читается и понятно организован\n\n"
                                      "2. Функциональность проекта соответствует задаче заказчика.\n\n"
                                      "3. Код запускается и не выдает ошибку при попытке его запустить или как-либо "
                                      "взаимодействовать с ним.\n\n"
                                      "4. Присутствует документация к проекту.\n\n"
                                      "5. Функции реализованы без багов и работают так, "
                                      "как описаны в документации к проекту.", parse_mode="html")

    bot.register_next_step_handler(message, send_project, link, difficulty)


def send_project(message, link, difficulty):
    rules = message.text

    user_id = message.from_user.id

    data = {
            "user_id": user_id,
            "project_link": link,
            "project_difficulty": difficulty}

    if rules != "1":
        data["rules"] = str(rules)

    resp = requests.post(
        url=basic_url + "projects/find-pair-or-create-project",
        json=data)

    status = resp.status_code

    if status == 400:
        resp = resp.json()["detail"]["message"]

        if "review" in resp:
            bot.send_message(message.chat.id, "Прежде чем отправить следующий проект, дождитесь, "
                                              "когда будет проверен предыдущий. Обычно это занимает не более 24 часов.",
                             reply_markup=send_review_keyboard)

        elif "github" in resp:
            bot.send_message(message.chat.id, "Ссылка, которую вы отправили, не ведет на github.",
                             reply_markup=send_project_keyboard)
            get_project_link(message)
            return

        elif "error" in resp:
            bot.send_message(message.chat.id, "Не получилось открыть вашу ссылку. Попробуйте снова.",
                             reply_markup=send_project_keyboard)

        else:
            bot.send_message(message.chat.id, "Другой ваш проект уже был отправлен."
                                              " Дождитесь его ревью прежде чем отправить следующий, "
                                              "либо удалите его, используя команду /delete_project или с помощью кнопки"
                                              ' "Удалить проект".', reply_markup=delete_project_keyboard)

    if status == 422:
        bot.send_message(message.chat.id, "Уровень сложности должен быть числом от 1 до 10.",
                         reply_markup=send_project_keyboard)
        get_project_link(message)
        return

    if status == 404:
        bot.send_message(message.chat.id, "Не удалось найти проект по отправленной ссылке. "
                                          "Убедитесь, что отправили верную ссылку.", reply_markup=send_project_keyboard)
        get_project_link(message)
        return

    if status == 403:
        bot.send_message(message.chat.id, "Кажется, вы не авторизованы, поэтому вы не можете отправить проект. "
                                          "Чтобы авторизоваться, используйте команду /register или кнопку"
                                          ' "Зарегистрироваться"', reply_markup=register_keyboard)

    if status == 201:
        bot.send_message(message.chat.id, "Ваш проект успешно добавлен в очередь на ревью. "
                                          "Когда наступит ваша очередь, вам придет уведомление.",
                         reply_markup=delete_project_keyboard)

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
            bot.send_message(chat_id=user, text="Пара для ревью успешно найдена. Можете начать работу над ним."
                                                " Примечание:\nВаше ревью должно состоять "
                                                "минимум из <b>70 символов</b> и содержать в себе "
                                                "<b>все критерии</b>, описанные ниже.",
                             reply_markup=send_review_keyboard, parse_mode="html")

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
        bot.send_message(message.chat.id, "Ваш проект успешно удален.", reply_markup=send_project_keyboard)

    if status == 404:
        bot.send_message(message.chat.id, "На данный момент у вас нет ни одного проекта в базе данных.",
                         reply_markup=send_project_keyboard)


@bot.message_handler(commands=["send_review"])
@bot.message_handler(content_types=["text"], func=lambda message: message.text.lower() == "отправить ревью")
def get_review(message):
    bot.send_message(message.chat.id, "Можете отправить ваше  <b>ревью: </b>", parse_mode="html")
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
        bot.send_message(message.chat.id, "Кажется, вы не авторизованы, поэтому вы не можете отправить проект. "
                                          "Чтобы авторизоваться, используйте команду /register или кнопку"
                                          ' "Зарегистрироваться"', reply_markup=register_keyboard)

    if status == 404:
        resp = resp.json()["detail"]["message"]

        if "pair" in resp:
            bot.send_message(message.chat.id, "Ваша очередь еще не подошла, поэтому у вас пока нет пары для ревью.",
                             reply_markup=delete_project_keyboard)

        if "project" in resp:
            bot.send_message(message.chat.id, "На данный момент у вас нет ни одного проекта в базе данных.",
                             reply_markup=send_project_keyboard)

    if status == 422:
        bot.send_message(message.chat.id, "Ваше ревью слишком короткое. Попробуйте снова.")
        get_review(message)
        return

    if status == 201:
        bot.send_message(message.chat.id, "Ваше ревью успешно добавлено в базу данных. "
                                          "Когда ваш напарник осуществит ревью вашего проекта, вы сможете обменяться "
                                          "ими. Если хотите удалить его, используйте команду /delete_review или кнопку"
                                          ' "Удалить ревью"', reply_markup=delete_review_keyboard)

    if status == 200:
        resp = resp.json()["reviews"]
        user_id_1 = resp["user_id_1"]
        review_1 = resp["review_for_1"]

        user_id_2 = resp["user_id_2"]
        review_2 = resp["review_for_2"]

        for user in [user_id_1, user_id_2]:
            bot.send_message(chat_id=user, text=f" <b>Ревью вашего проекта успешно выполнено! </b>",
                             reply_markup=send_project_keyboard, parse_mode="html")

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
        bot.send_message(message.chat.id, "Ваше ревью успешно удалено.", reply_markup=send_review_keyboard)

    if status == 404:
        bot.send_message(message.chat.id, "На данный момент вы не находитесь в паре для ревью.")


bot.infinity_polling()
