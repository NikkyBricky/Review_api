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