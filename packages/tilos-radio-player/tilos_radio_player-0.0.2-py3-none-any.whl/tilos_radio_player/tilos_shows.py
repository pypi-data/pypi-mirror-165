import json
from .tilos_interactive import SHOWS_FILE

with open(SHOWS_FILE, "r") as f:
    raw = "".join(f.readlines())
    SHOWS = json.loads(raw)
