import json

"""
    Useful Json methods for reading and writing the report files
"""

def save_json_report(record: dict, filename: str):
    with open(filename, "w") as f:
        f.write(json.dumps(record, indent = 4))

def load_json(filename: str) -> dict:
    with open(filename, "r") as f:
        report = json.load(f)
        return report