from fastapi import FastAPI
from api_v1 import router as router_v1
from core.config import settings
import uvicorn

description = """
ReviewApp API will help people do peer-to-peer reviews of their projects. 🚀

## Users

You will be able to:

* **Create users** (user_id is usually telegram id).
* **Login users** 
* **Delete users** 

You **can`t** delete user if he has a pair for review. 
Otherwise this rout will delete user and his project if he has one. 

## Projects

You will be able to:

* **Create projects** 
* **Delete projects** 

This object requires project difficulty which can be set with your terms.

If there is no project with the same project difficulty in the database, it will be added to it. 

Otherwise the data of
this project and of that one with the same project difficulty from the database will returned. Then the program 
deletes the project from database and creates a pair for review with this users.

Only **authorised** users can interact with this object. 

## Reviews

You will be able to:

* **Send reviews** 
* **Delete reviews** 

If one person from the pair sends a review, the program finds out whether the latter has it too. 

If it is False, the review will be added to database. Otherwise the reviews from ths pair will be returned.

Only **authorised** users can interact with this object. 
"""


app = FastAPI(
    title="Review API",
    description=description,
    summary="ReviewApp finds a pair of users who have projects with the same project difficulty."
            " Then it allows this users to review their work and send the results to each other. ")

app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


@app.get("/")
def start_message():
    return {"message": "Hi there! This is an api for reviewing projects."}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
