# BM Tracker Backend

A lightweight Flask backend to store and load tracker data in JSON format.

## Endpoints

- `GET /load` → returns the current tracker.json contents
- `POST /save` → saves new tracker.json from request body
- `GET /` → health check message

## Deployment on Render

1. Create a new Web Service on [Render](https://render.com).
2. Connect this GitHub repo.
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python server.py`
4. Deploy! You’ll get a public URL like:
