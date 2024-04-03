import uvicorn
from api_bot.bot import bot
from multiprocessing import Process
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H",
    filemode="w",
    force=True
)

def start_bot():
    bot.polling(none_stop=True)


def start_api():
    uvicorn.run("main:app", reload=True, port=5000)


if __name__ == "__main__":
    api = Process(target=start_api)
    api.start()
    logging.info("Апи запущено")
    print("Апи запущено")
    api_bot = Process(target=start_bot)
    api_bot.start()
    logging.info("Бот запущен")
    print("Бот запущен")
