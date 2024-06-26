from fastapi import FastAPI
from api_v1 import router as router_v1
from core.config import settings
from core.api_description import TITLE, DESCRIPTION, SUMMARY, VERSION

app = FastAPI(
    title=TITLE,
    description=DESCRIPTION,
    summary=SUMMARY,
    version=VERSION)

app.include_router(router=router_v1, prefix=settings.api_v1_prefix)
