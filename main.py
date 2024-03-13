from fastapi import FastAPI
from api_v1 import router as router_v1
from core.config import settings
from api_description import description, summary, version, title

app = FastAPI(
    title=title,
    description=description,
    summary=summary,
    version=version)

app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


@app.get("/")
def start_message():
    return {"message": "Hi there! This is an api for reviewing projects."}
