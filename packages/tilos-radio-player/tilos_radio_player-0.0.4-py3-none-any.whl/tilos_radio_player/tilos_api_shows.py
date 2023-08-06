"""Refreshes the shows JSON file with actual API data."""
import json
import requests
from .tilos_interactive import SHOWS_FILE


def update_shows():
    res = requests.get("https://tilos.hu/api/show")
    src = json.loads(res.text)

    with open(SHOWS_FILE, "w") as f:
        shows = {}

        for show in src:
            shows[show["alias"]] = show

        json_shows = json.dumps(shows)
        f.write(json_shows)

