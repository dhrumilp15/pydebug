import json

def save_json_report(record: dict, filename: str):
    with open(filename, "w") as f:
        f.write(json.dumps(record, indent = 4))

def load_json(filename: str):
    with open(filename, "r") as f:
        data = json.load(f)
        # print(data)
        return data