import json


def read_json(name):
    with open("config.json", 'r', encoding="utf-8") as file:
        data = json.load(file) 
        return data[name]