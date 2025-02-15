from fastapi import FastAPI, HTTPException, BackgroundTasks
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TELEX_API_KEY = os.getenv("TELEX_API_KEY")
TELEX_CHANNEL_ID = os.getenv("TELEX_CHANNEL_ID")
TELEX_BASE_URL = "https://api.telex.im/v1/channels"

app = FastAPI()

def send_message(content: str):
    """Send a message to the Telex.im channel."""
    headers = {"Authorization": f"Bearer {TELEX_API_KEY}"}
    data = {"content": content}
    response = requests.post(f"{TELEX_BASE_URL}/{TELEX_CHANNEL_ID}/messages", json=data, headers=headers)
    if response.status_code != 201:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()

@app.post("/send")
def send_notification(message: str, background_tasks: BackgroundTasks):
    """Send a notification message in the background."""
    background_tasks.add_task(send_message, message)
    return {"status": "Message queued for sending"}

@app.get("/channel")
def get_channel_info():
    """Retrieve channel details."""
    headers = {"Authorization": f"Bearer {TELEX_API_KEY}"}
    response = requests.get(f"{TELEX_BASE_URL}/{TELEX_CHANNEL_ID}", headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()

@app.post("/subscribe")
def subscribe_user(user_id: str):
    """Subscribe a user to the channel."""
    headers = {"Authorization": f"Bearer {TELEX_API_KEY}"}
    data = {"user_id": user_id}
    response = requests.post(f"{TELEX_BASE_URL}/{TELEX_CHANNEL_ID}/subscribers", json=data, headers=headers)
    if response.status_code != 201:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


{
  "data": {
    "date": {
      "created_at": "2025-02-08",
      "updated_at": "2025-02-08"
    },
    "descriptions": {
      "app_name": "TestINtegrator",
      "app_description": "test integration",
      "app_logo": "test.com/test.png",
      "app_url": "http://localhost",
      "background_color": "#fff"
    },
    "is_active": true,
    "integration_type": "text",
    "key_features": [
      "\"creates  a simple test json\"",
      "\"just kidding\""
    ],
    "author": "AYo",
    "settings": [
      {
        "label": "http://localhost/healthcheck",
        "type": "text",
        "required": true,
        "default": "active"
      }
    ],
    "target_url": "http://localhost",
    "tick_url": "http://localhost"
  }
}