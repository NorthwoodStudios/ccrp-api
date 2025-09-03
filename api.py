import flask
from flask import Flask
import asyncio
import requests
import time

app = Flask(__name__)

data = {
    "PlayerCount":0,
    "Join-Key":"PlaceHolder"
}

@app.route('/')
async def alive():
    return "WE ARE ALIVE!!!!!!"

@app.route('/ccrp/api/playercount')
async def getcount():
    pc = data["PlayerCount"]
    return pc

@app.route('/ccrp/api/join-key')
async def getkey():
    pc = data["Join-Key"]
    return pc

async def GetData():
    while True:
        try:
            response = requests.get(
                "https://api.policeroleplay.community/v1/server",
                headers={
                    "server-key": "zFimkdNGhQtakddpurJb-GNHkdJZiZqzVkIZMxMZhYfeFjbIItHDFmYwNRBGJ",
                    "Accept": "*/*"
                },
                timeout=5
            )

            if response.status_code == 200:
                result = response.json()
                data["Join-Key"] = result.get("JoinKey", "")
                data["PlayerCount"] = result.get("CurrentPlayers", 0)
                print(f"Updated: {data}")
            else:
                print(f"Error: Status code {response.status_code}")

        except Exception as e:
            print("Request failed:", e)

        # Sleep 10 seconds between requests to avoid rate limiting
        time.sleep(10)
        


asyncio.create_task(GetData())






