from fastapi import FastAPI
from api_v1 import router as router_v1
from core.config import settings
from api_description import description


app = FastAPI(
    title="Review API",
    description=description,
    summary="ReviewApp finds a pair of users who have projects with the same project difficulty."
            " Then it allows this users to review their work and send the results to each other. ",
    version="0.0.1")

app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


@app.get("/")
def start_message():
    return {"message": "Hi there! This is an api for reviewing projects."}
