from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

data = {}

class UploadData(BaseModel):
    heading: str
    description: str


class UpdateData(BaseModel):
    heading: str
    new_heading: str
    new_description: str


class DeleteData(BaseModel):
    heading: str


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


@app.post("/upload")
async def upload_data(new_data: UploadData):
    data[new_data.heading] = new_data.description

    return {"message": "Data uploaded successfully", "data": data}


# im unsure how to handle this
# rn it just requires a heading, a new_heading, and a description
# if someone wants to change only description and keep heading the same,
# then they can pass the same value for heading and new_heading
@app.post("/update")
async def update_data(new_data: UpdateData):
    if new_data.heading not in data:
        raise HTTPException(status_code=404, detail="Heading not found")

    # delete old heading
    data.pop(new_data.heading)

    # create data again with new heading
    data[new_data.new_heading] = new_data.new_description

    return {"message": "Data updated successfully", "data": data}


@app.post("/delete")
async def delete_data(delete_request: DeleteData):
    if delete_request.heading not in data:
        raise HTTPException(status_code=404, detail="Heading not found")

    data.pop(delete_request.heading)

    return {"message": "Data deleted successfully", "data": data}
