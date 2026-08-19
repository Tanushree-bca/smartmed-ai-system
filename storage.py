import json
import os

DATA_FILE = "smartmed_data.json"


def load_history():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_record(record):
    history = load_history()
    history.append(record)
    with open(DATA_FILE, "w") as f:
        json.dump(history, f, indent=2)
