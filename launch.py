import uvicorn
from api_bot.bot import bot
from multiprocessing import Process


def start_bot():
    bot.polling(none_stop=True)


def start_api():
    uvicorn.run("main:app", reload=True, port=8000)


if __name__ == "__main__":
    api = Process(target=start_api)
    api.start()
    bot = Process(target=start_bot)
    bot.start()

