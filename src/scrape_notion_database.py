import requests
import json

# load json "../secrets.json"
with open("./secrets.json") as f:
    secrets = json.load(f)
    NOTION_TOKEN = secrets["notion_secret"]
    databases = secrets["databases"]

header = headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

payload = {"page_size": 100}

notes_id = databases[1]["id"]

response = requests.post(f"https://api.notion.com/v1/databases/{notes_id}/query", headers=header, json=payload)

data = response.json()

print(data)