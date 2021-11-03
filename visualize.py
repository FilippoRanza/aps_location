#! /usr/bin/python

""" 
Generate a plot from aps_loc output.
"""

from argparse import ArgumentParser
import json

import numpy as np
from matplotlib import pyplot as plt


def radii_to_str(radii):
    r1, r2 = radii
    key = f"$r_1: {r1},\ r_2: {r2}$"
    return key


def load_instance(file_name):
    with open(file_name) as file:
        data = json.load(file)

    output = {radii_to_str(radii): np.array(vals) for radii, vals in data}
    return output


def plot_one_figure(inst: dict):
    legend = []
    for k, v in inst.items():
        legend.append(k)
        x = np.arange(1, len(v) + 1)
        plt.plot(x, v, "o-.")
    plt.legend(legend)
    plt.xticks(x)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--title", help="set image title")
    parser.add_argument("log_file", help="output file from asp_loc.py")
    return parser.parse_args()


def main():
    args = parse_args()
    logs = load_instance(args.log_file)
    plot_one_figure(logs)
    if args.title:
        plt.title(args.title)

    plt.show()


if __name__ == "__main__":
    main()
