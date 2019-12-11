import json


def json_reader():
    with open("data.json", "r") as file:
        return json.load(file)


def json_writer(data):
    with open("data.json", "w") as file:
        return json.dump(data, file, indent=2)
