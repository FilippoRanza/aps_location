#! /usr/bin/python

import json

import numpy as np


def load_json_file(file_name):
    with open(file_name) as file:
        data = json.load(file)
    return data

def to_ndarray(json_dict, name):
    value = json_dict[name]
    return np.array(value)
