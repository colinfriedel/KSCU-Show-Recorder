import requests
import json
from datetime import datetime, timedelta
import pytz

API_KEY = "fsr9w2R8irUUqUkze_QUcyB3"
STATION_ID = "KSCU"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def get_persona_info(persona_id):
    """Fetch persona info by ID (name and email)"""
    url = f"https://spinitron.com/api/personas/{persona_id}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return {
            "name": data.get("name", "Unknown"),
            "email": data.get("email", "")
        }
    except requests.HTTPError:
        return {"name": "Unknown", "email": ""}

def download_week_schedule():
    local = pytz.timezone("America/Los_Angeles")
    now_utc = datetime.now(pytz.utc)
    end_utc = now_utc + timedelta(days=7)

    url = "https://spinitron.com/api/shows"
    params = {
        "station": STATION_ID,
        "start": now_utc.isoformat(),
        "end": end_utc.isoformat(),
        "count": 200
    }

    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()

    schedule = []
    persona_cache = {}  # persona_id -> {name, email}

    for show in data["items"]:
        show_id = show.get("id")
        title = show.get("title", "Untitled Show")
        start = datetime.fromisoformat(show["start"]).astimezone(local)
        end = datetime.fromisoformat(show["end"]).astimezone(local)

        # Try to get persona ID from _links
        persona_links = show.get("_links", {}).get("personas", [])
        if persona_links:
            persona_href = persona_links[0].get("href", "")
            persona_id = int(persona_href.rstrip("/").split("/")[-1]) if persona_href else None
        else:
            persona_id = None

        # Lookup persona info
        if persona_id:
            if persona_id not in persona_cache:
                persona_cache[persona_id] = get_persona_info(persona_id)
            dj = persona_cache[persona_id]
        else:
            dj = {"name": "Unknown", "email": ""}

        schedule.append({
            "title": title,
            "day": start.strftime("%A"),
            "start_time": start.strftime("%H:%M"),
            "end_time": end.strftime("%H:%M"),
            "dj_name": dj["name"],
            "dj_email": dj["email"]
        })

    with open("schedule.json", "w") as f:
        json.dump(schedule, f, indent=2)
    print(f"Saved {len(schedule)} shows to schedule.json")

# Run it
download_week_schedule()
