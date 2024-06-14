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

notes_id = databases[1]["id"]

def get_db_pages(database_id, header, num_pages=None):
    
    assert num_pages is None or 0 < num_pages < 101, "num_pages must be None or a positive integer (0, 100]"

    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    
    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}

    response = requests.post(url, headers=header, json=payload)
    data = response.json()

    results = data["results"]

    while data["has_more"] and get_all:
        payload["start_cursor"] = data["next_cursor"]

        response = requests.post(url, headers=header, json=payload)
        data = response.json()
        
        results.extend(data["results"])

    return results

notes = get_db_pages(notes_id, header)

with open('db.json', 'w', encoding='utf8') as f:
    json.dump(notes, f, ensure_ascii=False, indent=4)
