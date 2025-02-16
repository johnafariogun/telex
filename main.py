from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse

from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import requests
from pydantic import BaseModel
from typing import List
import httpx
import asyncio


app = FastAPI()
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["GET"],
        allow_headers=["*"],
        allow_credentials=True,
    )

@app.get("/integration.json")
def get_integration_json(request: Request):
    base_url = str(request.base_url).rstrip("/")
    return {
        "data": {
            "descriptions": {
                "app_name": "Uptime Monitor",
                "app_description": "Monitors website uptime",
                "app_url": base_url,
                "app_logo": "https://i.imgur.com/lZqvffp.png",
                "background_color": "#fff"
            },
            "integration_type": "interval",
            "integration_category": "Website Uptime",
            "key_features": [
            "\"checks uptime\""
            ],
            "settings": [
                {"label": "site-1", "type": "text", "required": True, "default": ""},
                {"label": "site-2", "type": "text", "required": True, "default": ""},
                {"label": "interval", "type": "text", "required": True, "default": "* * * * *"}
            ],
            "tick_url": f"{base_url}/tick"
        }
    }


class Setting(BaseModel):
    label: str
    type: str
    required: bool
    default: str

class MonitorPayload(BaseModel):
    channel_id: str
    return_url: str
    settings: List[Setting]

async def check_site_status(site: str) -> str:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(site, timeout=10)
            if response.status_code < 400:
                return None
            return f"{site} is down (status {response.status_code})"
    except Exception as e:
        return f"{site} check failed: {str(e)}"

async def monitor_task(payload: MonitorPayload):
    sites = [s.default for s in payload.settings if s.label.startswith("site")]
    results = await asyncio.gather(*(check_site_status(site) for site in sites))

    message = "\n".join([result for result in results if result is not None])

    # data follows telex webhook format. Your integration must call the return_url using this format
    data = {
        "message": message,
        "username": "Uptime Monitor",
        "event_name": "Uptime Check",
        "status": "error"
    }

    async with httpx.AsyncClient() as client:
        await client.post(payload.return_url, json=data)




@app.post("/tick", status_code=202)
def monitor(payload: MonitorPayload, background_tasks: BackgroundTasks):
    background_tasks.add_task(monitor_task, payload)
    return {"status": "accepted"}

@app.get('/')
async def get_info():
    current_datetime = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

    return {
        "email": "afariogunjohn2502@gmail.com",
        "current_datetime": current_datetime,
        "github_url": "https://github.com/johnafariogun/HNG12"
    }



# Helper function to check if a number is prime
def is_prime(num: int) -> bool:
    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

# Helper function to check if a number is a perfect number
def is_perfect(num: int) -> bool:
    divisors = [i for i in range(1, num) if num % i == 0]
    return sum(divisors) == num

# Helper function to check if a number is Armstrong
def is_armstrong(num: int) -> bool:
    digits = [int(digit) for digit in str(num)]
    return num == sum([digit ** len(digits) for digit in digits])

# Helper function to sum digits of a number
def digit_sum(num: int) -> int:
    return sum([int(digit) for digit in str(num)])

# Helper function to get fun fact from Numbers API
def get_fun_fact(num: int) -> str:
    response = requests.get(f"http://numbersapi.com/{num}?json&math=true")
    if response.status_code == 200:
        return response.json().get("text", "No fun fact found.")
    return "No fun fact found."

@app.get("/api/classify-number")
async def classify_number(number: int):
    # Check if the number is a valid integer
    if not isinstance(number, int):
        raise HTTPException(status_code=400, detail="Invalid input. Please provide an integer.")
    
    # Determine properties of the number
    is_armstrong_number = is_armstrong(number)
    is_odd = number % 2 != 0
    is_even = not is_odd
    is_prime_number = is_prime(number)
    is_perfect_number = is_perfect(number)
    properties = []

    if is_armstrong_number:
        properties.append("armstrong")
    if is_odd:
        properties.append("odd")
    else:
        properties.append("even")

    # Get digit sum
    digit_sum_value = digit_sum(number)

    # Get fun fact from Numbers API
    fun_fact = get_fun_fact(number)

    # Return JSON response
    return JSONResponse(content={
        "number": number,
        "is_prime": is_prime_number,
        "is_perfect": is_perfect_number,
        "properties": properties,
        "digit_sum": digit_sum_value,
        "fun_fact": fun_fact
    })

# Catch any invalid or missing parameters
@app.exception_handler(HTTPException)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"number": str(request.query_params.get('number')), "error": True},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
