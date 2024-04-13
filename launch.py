import uvicorn
from multiprocessing import Process


def start_api():
    uvicorn.run("main:app", reload=True, port=8000)


if __name__ == "__main__":
    api = Process(target=start_api)
    api.start()
