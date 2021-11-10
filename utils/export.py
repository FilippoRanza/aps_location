#! /usr/bin/python

import json

def export_results(file_name, **kwargs):
    with open(file_name, "w") as file:
        json.dump(kwargs, file)

