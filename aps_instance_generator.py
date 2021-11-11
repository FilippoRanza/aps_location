#! /usr/bin/python

"""
Generate a sample instance 
"""

import json
import secrets
import sys

from matplotlib import pyplot as plt
import numpy as np

import generator as gen




def show_points(points):
    X = []
    Y = []
    for x, y in points:
        X.append(x)
        Y.append(y)
    plt.scatter(X, Y)


def make_instance(lambda_coeff, distances):

    distance = distances.tolist()
    instance = {"lambda_coeff": lambda_coeff, "distances": distance}
    return json.dumps(instance)


def make_location(clients, stops):
    clients = clients
    stops = stops
    locations = {"clients": clients, "stops": stops}
    return json.dumps(locations)


def round_distance(val, order):
    val = np.round(val).astype(np.int32)
    val -= val % order
    return val


def make_radius(distances, order):
    distances = round_distance(distances, order)
    count = {}
    for row in distances:
        for d in row:
            try:
                count[d] += 1
            except KeyError:
                count[d] = 1
    count_list = list(count.items())
    count_list.sort(key=lambda x: -x[1])
    radius_list = [int(x) for x, _ in count_list if x]
    radius_list.sort()
    return json.dumps(radius_list)


def show_instances(clients, stops):
    show_points(clients)
    show_points(stops)
    plt.show()


def main():
    client_conf = gen.ClientConfig(15, 150, 500, 2500)
    stop_conf = gen.StopConfiguration(20, 150, 1500, 1500)
    rnd_instance = gen.build_random_instance(stop_conf, client_conf)

    show_instances(rnd_instance.clients, rnd_instance.stops)

    radius_list = make_radius(rnd_instance.distances, 5000)
    instance = make_instance(rnd_instance.lambda_coeff, rnd_instance.distances)
    locations = make_location(rnd_instance.clients, rnd_instance.stops)
    try:
        with open(sys.argv[1], "w") as file:
            print(instance, file=file)
        with open(sys.argv[2], "w") as file:
            print(locations, file=file)
        with open(sys.argv[3], "w") as file:
            print(radius_list, file=file)
    except IndexError:
        print(instance)


if __name__ == "__main__":
    main()
