import os
import requests
import time
from threading import Thread
from flask import Flask, jsonify

app = Flask(__name__)

data = {
    "PlayerCount": 0,
    "JoinKey": "PlaceHolder"
}

# Routes
@app.route("/")
def alive():
    return "WE ARE ALIVE!!!!!!"

@app.route("/ccrp/api/playercount")
def getcount():
    return jsonify({"CurrentPlayers": data["PlayerCount"]})

@app.route("/ccrp/api/joinkey")
def getkey():
    return jsonify({"JoinKey": data["JoinKey"]})

# Background data fetch
def GetData():
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
                data["JoinKey"] = result.get("JoinKey", "")
                data["PlayerCount"] = result.get("CurrentPlayers", 0)
                print(f"Updated: {data}")
            else:
                print(f"Error: Status code {response.status_code}")

        except Exception as e:
            print("Request failed:", e)

        time.sleep(10)  # Update every 10 seconds

# Start background thread
Thread(target=GetData, daemon=True).start()

# Run Flask app on Render's port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
