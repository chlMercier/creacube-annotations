import json

CONFIGURATIONS = {}

with open("configurations.json", "r", encoding="UTF-8") as config:
    CONFIGURATIONS = json.load(config)