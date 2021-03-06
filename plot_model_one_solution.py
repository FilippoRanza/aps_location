#! /usr/bin/python

"""
Plot the soluton from Model one
"""
from argparse import ArgumentParser

import numpy as np
import matplotlib
from matplotlib import pyplot as plt

from utils import load_json_file, to_ndarray


def random_color():
    return np.random.random((1, 3))


def find_assignment(client_assignment):
    selected = client_assignment == 1
    indexes = [i for i in range(len(selected)) if selected[i]]
    if indexes:
        return np.random.choice(indexes, 1)[0] 
    return None


def make_assignment(solution):
    for i, client_assignment in enumerate(solution):
        sel = find_assignment(client_assignment)
        if sel:
            yield (i, sel)


def plot_stops(stops, selected_stops):
    color_sel = {}
    for i, (sel, (x, y)) in enumerate(zip(selected_stops, stops)):
        if sel:
            marker = "s"
            color = random_color()
            color_sel[i] = color
        else:
            marker = "o"
            color = "k"

        plt.scatter([x], [y], marker=marker, c=color, s=105)
    return color_sel


class ClientCoordinate:
    def __init__(self, p):
        x, y = p
        self.x = [x]
        self.y = [y]

    def add_point(self, p):
        x, y = p
        self.x.append(x)
        self.y.append(y)


def plot_client(colors, client_loc, solution):
    client_sel = {}
    for i, sel in make_assignment(solution):

        try:
            client_sel[sel].add_point(client_loc[i])
        except KeyError:
            client_sel[sel] = ClientCoordinate(client_loc[i])

    for sel, coord in client_sel.items():
        plt.scatter(coord.x, coord.y, marker=".", c=colors[sel], s=35)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("locations", help="set location JSON file")
    parser.add_argument("solution", help="set solution file")
    parser.add_argument("--title", help="set image title", default="")
    parser.add_argument("--file", help="save image to file", default=None)

    return parser.parse_args()

def set_plot_relative_size(delta_w, delta_h):
    w, h = plt.rcParams["figure.figsize"]
    w *= delta_w
    h *= delta_h
    plt.rcParams["figure.figsize"] = (w, h)  

def main():
    font = {'family' : 'normal',
        'size'   : 22}

    matplotlib.rc('font', **font)
    set_plot_relative_size(4, 4)
    args = parse_args()
    locations = load_json_file(args.locations)
    stops = to_ndarray(locations, "stops")
    clients = to_ndarray(locations, "clients")

    solution = load_json_file(args.solution)
    selected_stops = to_ndarray(solution, "y")
    solution = to_ndarray(solution, "x")

    colors = plot_stops(stops, selected_stops)
    plot_client(colors, clients, solution)

    if args.title:
        plt.title(args.title)

    plt.tight_layout()

    if args.file:
        plt.savefig(args.file)
    else:
        plt.show()


if __name__ == "__main__":
    main()
