import json
import os


def save_status(json_file, objects):
    if len(objects) > 0:
        with open(json_file, "w") as f:
            json.dump(objects, f, indent=4)
    else:
        if os.path.isfile(json_file):
            os.remove(json_file)


def load_status(json_file):
    with open(json_file, "r") as f:
        data = json.load(f)

    return data
