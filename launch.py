import uvicorn
from api_bot.bot import run_bot
from multiprocessing import Process
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H"
)


def start_api():
    uvicorn.run("main:app", reload=True, port=8000)


if __name__ == "__main__":
    api = Process(target=start_api)
    api.start()
    logging.info("Апи запущено")

    api_bot = Process(target=run_bot)
    api_bot.start()
    logging.info("Бот запущен")
