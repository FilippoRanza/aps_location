#! /usr/bin/python

"""

"""

from dataclasses import dataclass

import numpy as np


@dataclass
class RandomInstance:
    stops: [(int, int)]
    clients: [(int, int)]
    distances: [[float]]
    lambda_coeff: [float]


def make_clients(station, count, scale):
    sx, sy = station
    points = set()
    while len(points) < count:
        x = (np.random.normal() * scale) + sx
        y = (np.random.normal() * scale) + sy
        points.add((x, y))
    return list(points)


def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    a = (x1 - x2) ** 2
    b = (y1 - y2) ** 2
    return np.sqrt(a + b)


def build_distance_matrix(clients, stations):
    output = np.zeros((len(clients), len(stations)))
    for i, c in enumerate(clients):
        for j, s in enumerate(stations):
            output[i, j] = distance(c, s)
    return output

@dataclass
class StopConfiguration:
    count: int
    delta_x: int
    delta_y: int
    distance: int


def gen_stops(sc: StopConfiguration):
    stops = []
    x = 0
    while len(stops) < sc.count:
        y = x + np.random.randint(-sc.delta_y, sc.delta_y)
        x_tmp = x + np.random.randint(-sc.delta_x, sc.delta_x)
        stops.append((x_tmp, y))
        x += sc.distance
    return stops

@dataclass
class ClientConfig:
    min_count: int
    max_count: int
    min_scale: int
    max_scale: int


def gen_client(cc: ClientConfig, stops):

    clients = []
    lambda_coeff = []
    for s in stops:
        amt = np.random.randint(cc.min_count, cc.max_count)
        lambda_coeff.append(amt)
        scale = np.random.randint(cc.min_scale, cc.max_scale)
        tmp = make_clients(s, amt, scale)
        clients += tmp

    return clients, lambda_coeff


def build_random_instance(stop_conf: StopConfiguration, client_conf: ClientConfig):
    stops = gen_stops(stop_conf)
    clients, lambda_coeff = gen_client(client_conf, stops)
    distances = build_distance_matrix(clients, stops)
    return RandomInstance(stops, clients, distances, lambda_coeff)
