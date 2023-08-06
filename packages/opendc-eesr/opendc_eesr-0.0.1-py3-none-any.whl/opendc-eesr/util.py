import json
import subprocess
from uuid import uuid5, NAMESPACE_DNS
from time import time_ns


def load_json(path):
    with open(path, "r") as read_file:
        return json.load(read_file)


def generate_unique_id(input_dict):
    name = json.dumps(input_dict) + str(time_ns())
    return uuid5(NAMESPACE_DNS, name)


def inline(path="report.html"):
    subprocess.run(["node", "reporting/inliner.js", path])
