import requests as req
import time
from dateutil import parser
from datetime import datetime, timezone
from urllib import parse
import json

# Load config in
config = json.load(open("config.json"))


# Functions
def check_date(date: datetime):
    now = datetime.now(timezone.utc)
    if date.year == now.year and date.month == now.month and date.day == now.day and date.hour == now.hour:
        if abs(date.minute - now.minute) <= 3:
            return True
        else:
            return False
    else:
        return False


def check_activity(player_tag: str) -> bool:
    url = f"https://api.brawlstars.com/v1/players/{parse.quote(player_tag)}/battlelog"
    auth = {"Authorization": config["Api_key"]}

    response = req.get(url, headers=auth).json()
    date = parser.isoparse(response["items"][0]["battleTime"])

    return check_date(date)


def notify(webhook, player_id):
    url = f"https://api.brawlstars.com/v1/players/{parse.quote(player_id)}"
    auth = {"Authorization": config["Api_key"]}

    player_name = req.get(url, headers=auth).json()["name"]

    message = {
        "content": "",
        "tts": False,
        "embeds": [
            {
                "id": 533329316,
                "description": f"Player: {player_name}",
                "fields": [],
                "title": "Player Online",
                "color": 16773120,
                "thumbnail": {
                    "url": "https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9XYWpVOVRURjRmUjZvaXJoelRycC5wbmcifQ:supercell:q-JjkUtfOXZKDL5mlLVxomeguw7fQqJ7TocMs_XbF6o?width=2400"
                }
            }
        ],
        "components": [],
        "actions": {}
    }

    req.post(webhook, json=message)


while True:
    for player in config["Players"]:
        print(f"Checking: {player}")
        if check_activity(player):
            notify(config["Webhook_url"], player)
            print("Online")
        time.sleep(5)
    time.sleep(60)
