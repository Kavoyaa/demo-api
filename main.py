from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# username: password
creds = {}

# heading: [description, username]
data = {}


# returns error if invalid, otherwise it returns nothing
def login(username: str, password: str):
    correct_password = creds.get(username)

    if correct_password is None:
        raise HTTPException(status_code=401, detail="Incorrect Username!")

    if correct_password != password:
        raise HTTPException(status_code=401, detail="Incorrect Password!")


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
async def login_user(username: str, password: str):
    correct_password = creds.get(username)

    if correct_password is None:
        creds[username] = password
        return {"message": "Register successful"}

    if correct_password == password:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Password Incorrect")


@app.post("/upload")
async def upload_data(username: str, password: str, heading: str, description: str):
    # here's where the AUTH is important!
    login(username, password)

    data[heading] = [description, username]

    return {"message": "Data uploaded successfully", "data": data}


@app.post("/update")
async def update_data(
    username: str,
    password: str,
    heading: str,
    new_heading: str,
    new_description: str,
):
    login(username, password)

    if heading not in data:
        raise HTTPException(status_code=404, detail="Heading not found")

    description, post_username = data[heading]

    if post_username != username:
        raise HTTPException(status_code=403, detail="Not your heading")

    if new_heading != heading and new_heading in data:
        raise HTTPException(status_code=409, detail="Heading already exists")

    # delete old heading
    data.pop(heading)

    # create data again with new heading
    data[new_heading] = [new_description, username]

    return {"message": "Data updated successfully", "data": data}


@app.post("/delete")
async def delete_data(username: str, password: str, heading: str):
    login(username, password)

    if heading not in data:
        raise HTTPException(status_code=404, detail="Heading not found")

    description, post_username = data[heading]

    if post_username != username:
        raise HTTPException(status_code=403, detail="Not your heading")

    data.pop(heading)

    return {"message": "Data deleted successfully", "data": data}


app.mount(
    "/",
    StaticFiles(directory=Path(__file__).parent / "workshop-js", html=True),
    name="frontend",
)