import json

_config = None


def get_config(config_name: str):
    with open(f"C:/Users/KacperK/Desktop/Xavier_ROV4/configs/{config_name}.json", "r") as f:
        config = json.load(f)

    return config