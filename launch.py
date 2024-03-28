import uvicorn
from bot import bot
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)
    bot.polling(none_stop=True)
