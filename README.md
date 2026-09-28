# demo-api
API for the demo project in OSDC's webdev workshop.

## Instructions for running

Create and enable virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies
```bash
pip install -r requirements.txt
```

Run the API
```bash
fastapi dev
```

The API will start running at `http://127.0.0.1:8000`.

## Running the demo
Make sure the API is running, and then,
```bash
python demo.py
```
