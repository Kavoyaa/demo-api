from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# username: password
creds = {}
# heading: [description, username]
data = {}


class LoginData(BaseModel):
    username: str
    password: str


class UploadData(LoginData):
    heading: str
    description: str


class UpdateData(LoginData):
    heading: str
    new_heading: str
    new_description: str


class DeleteData(LoginData):
    heading: str


def login(username: str, password: str):
    correct_password = creds.get(username)

    if correct_password is None:
        raise HTTPException(status_code=401, detail="Incorrect Username!")

    if correct_password != password:
        raise HTTPException(status_code=401, detail="Incorrect Password!")


@app.get("/")
async def root():
    return {"message": "Hello World"}


# no need auth for get data
@app.get("/data")
async def get_data():
    results = []
    for heading in data:
        discription, username = data[heading]
        results.append([heading, discription, username])

    return {"data": results}


@app.get("/search/{query}")
async def search_data(query: str):
    results = []
    for heading in data:
        discription, username = data[heading]

        if query.lower() in heading.lower():
            results.append([heading, discription, username])

        if query.lower() in discription.lower():
            results.append([heading, discription, username])

    return {"data": results}

# validates their credentials. if new username, it creates one.
@app.post("/login")
async def login_user(data: LoginData):
    correct_password = creds.get(data.username)

    if correct_password is None:
        creds[data.username] = data.password
        return {"message": "Register successful"}

    if correct_password == data.password:
        return {"message": "Login successful"}
    else:
        return {"message": "Password Incorrect"}


@app.post("/upload")
async def upload_data(new_data: UploadData):
    # here's where the AUTH is important!
    login(new_data.username, new_data.password)

    data[new_data.heading] = [new_data.description, new_data.username]

    return {"message": "Data uploaded successfully", "data": data}


# im unsure how to handle this
# rn it just requires a heading, a new_heading, and a description
# if someone wants to change only description and keep heading the same,
# then they can pass the same value for heading and new_heading
@app.post("/update")
async def update_data(new_data: UpdateData):
    login(new_data.username, new_data.password)

    if new_data.heading not in data:
        raise HTTPException(status_code=404, detail="Heading not found")

    # delete old heading
    data.pop(new_data.heading)

    # create data again with new heading
    data[new_data.new_heading] = [new_data.new_description, new_data.username]

    return {"message": "Data updated successfully", "data": data}


@app.post("/delete")
async def delete_data(delete_request: DeleteData):
    login(delete_request.username, delete_request.password)

    if delete_request.heading not in data:
        raise HTTPException(status_code=404, detail="Heading not found")

    data.pop(delete_request.heading)

    return {"message": "Data deleted successfully", "data": data}
