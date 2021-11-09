#! /usr/bin/python

import numpy as np


def compute_reach_coefficent(distances: np.ndarray, time: float):
    tmp = distances <= time
    return tmp.astype(np.int8)
