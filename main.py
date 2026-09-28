from fastapi import FastAPI

app = FastAPI()

data = {}

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/data")
async def get_data():
    response = []
    for key in data:
        response.append({key: data[key]})

    return {"data": response}

@app.get("/search/{query}")
async def search_data(query: str):
    results = []
    for key in data:
        if query.lower() in str(data[key]).lower():
            results.append({key: data[key]})

    return {"results": results}


# TODO: this will give error if the data isnt inputted in correct format
# i.e, {"heading": "something", "description": "blah blah blah"}
@app.post("/upload")
async def upload_data(new_data: dict):
    data[new_data["heading"]] = new_data["description"]

    return {"message": "Data uploaded successfully", "data": data}
