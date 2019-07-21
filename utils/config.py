import json

_config = None
with open("config.json", "r") as f:
    _config = json.load(f)

def get_config():
    return _config
