#! /usr/bin/python

from dataclasses import fields
import json

import numpy as np


def load_json_file(file_name):
    with open(file_name) as file:
        data = json.load(file)
    return data


def to_ndarray(json_dict, name):
    value = json_dict[name]
    return np.array(value)


def load_instance(kls, file_name):
    kls_fields = fields(kls)
    instance = load_json_file(file_name)
    conf = {f.name: to_ndarray(instance, f.name) for f in kls_fields}
    return kls(**conf)
