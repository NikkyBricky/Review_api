from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def start_message():
    return {"message": "Hi there! This is an api for reviewing projects."}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
