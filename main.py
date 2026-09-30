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


# returns error if invalid, otherwise it returns nothing
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
        description, username = data[heading]
        results.append([heading, description, username])

    return {"data": results}


@app.get("/search/{query}")
async def search_data(query: str):
    results = []

    for heading in data:
        description, username = data[heading]

        # Add the result only once, even if the query
        # appears in both heading and description.
        if (query.lower() in heading.lower()) or (query.lower() in description.lower()):
            results.append([heading, description, username])

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
        raise HTTPException(status_code=401, detail="Password Incorrect")


@app.post("/upload")
async def upload_data(new_data: UploadData):
    # here's where the AUTH is important!
    login(new_data.username, new_data.password)

    data[new_data.heading] = [new_data.description, new_data.username]

    return {"message": "Data uploaded successfully", "data": data}


@app.post("/update")
async def update_data(new_data: UpdateData):
    login(new_data.username, new_data.password)

    if new_data.heading not in data:
        raise HTTPException(status_code=404, detail="Heading not found")

    description, username = data[new_data.heading]

    if username != new_data.username:
        raise HTTPException(status_code=403, detail="Not your heading")

    if new_data.new_heading != new_data.heading and new_data.new_heading in data:
        raise HTTPException(status_code=409, detail="Heading already exists")

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

    description, username = data[delete_request.heading]

    if username != delete_request.username:
        raise HTTPException(status_code=403, detail="Not your heading")

    data.pop(delete_request.heading)

    return {"message": "Data deleted successfully", "data": data}
