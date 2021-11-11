#! /usr/bin/python

"""
Generate a sample instance 
"""

import secrets
import sys

from matplotlib import pyplot as plt
import numpy as np
import json

def place_points(count, width, height):
    points = set()
    while len(points) < count:
        x = secrets.randbelow(width)
        y = secrets.randbelow(height)
        points.add((x, y))
    return list(points)

def delta_vect(count, delta):
    output = np.zeros(count)
    for i in range(count):
        d = secrets.randbelow(2 * delta) - delta
        output[i] = d
    return output

def make_stops(count, width, height, delta):
    x = np.linspace(0, width, count) + delta_vect(count, delta)
    y = np.linspace(0, height, count) + delta_vect(count, delta)
    return list(zip(x, y))


def show_points(points):
    X = []
    Y = []
    for x, y in points:
        X.append(x)
        Y.append(y)
    plt.scatter(X, Y)


def euclid_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    x_dist = (x1 - x2) ** 2
    y_dist = (y1 - y2) ** 2
    return np.sqrt(x_dist + y_dist)

def make_distance_matrix(clients, stops):
    output = np.zeros((len(clients), len(stops)))
    for i, c in enumerate(clients):
        for j, s in enumerate(stops):
            output[i, j] = euclid_distance(c, s)
    return output

def make_lambda_coeff(stops, min_val, max_val):
    diff = max_val - min_val
    return [secrets.randbelow(diff) + min_val for _ in range(stops)]
    

def make_instance(lambda_coeff, distances):

    distance = distances.tolist()
    instance = {
        'lambda_coeff': lambda_coeff,
        'distances': distance
    }
    return json.dumps(instance)

def make_location(clients, stops):
    clients = clients
    stops = stops
    locations = {
        "clients": clients,
        "stops": stops
    }
    return  json.dumps(locations)

def round_distance(val, order):
    val = np.round(val).astype(np.int32)
    val -= (val % order)
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
    width = 100000
    height = 100000
    client_count = 1500
    clients = place_points(client_count, width, height)
    stop_count = 20
    stops = make_stops(stop_count, width, height, 4500)
    lambda_coeff = make_lambda_coeff(stop_count, 500, 17500)

    show_instances(clients, stops)

    distances = make_distance_matrix(clients, stops)
    radius_list = make_radius(distances, 5000)
    instance = make_instance(lambda_coeff, distances)
    locations = make_location(clients, stops)
    try:
        with open(sys.argv[1], "w") as file:
            print(instance, file=file)
        with open(sys.argv[2], "w") as file:
            print(locations, file=file)
        with open(sys.argv[3], "w") as file:
            print(radius_list, file=file)
    except IndexError:
        print(instance)

if __name__ == '__main__':
    main()
