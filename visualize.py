#! /usr/bin/python

""" 
Generate a plot from aps_loc output.
"""

from argparse import ArgumentParser
import json

import numpy as np
from matplotlib import pyplot as plt


def radii_to_str(radii):
    try:
        iter(radii)
    except TypeError:
        radii = [radii]
    radii = [f"r_{i}: {r}" for i, r in enumerate(radii)]
    key = r",\\".join(radii)
    key = "$" + key + "$"
    return key


def load_instance(file_name):
    with open(file_name) as file:
        data = json.load(file)

    output = {radii_to_str(radii): np.array(vals) for radii, vals in data}
    return output



def plot_one_figure(inst: dict, min_th, max_th):
    legend = []
    for k, v in inst.items():
        sel =  np.logical_and(min_th <= v, v <= max_th) 
        if sel.any():
            x = np.arange(1, len(v) + 1)
            x_sel = x[sel]
            v_sel = v[sel]
            legend.append(k)
            plt.plot(x_sel, v_sel, "o-.")

    plt.legend(legend)
    plt.grid(alpha=0.65, linestyle="dotted")
    plt.xticks(x)
    


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--title", help="set image title")
    parser.add_argument("log_file", help="output file from asp_loc.py")
    parser.add_argument("--min-threshold", help="set the minimal alpha to show. Default to 0.4", type=float, default=0.4)
    parser.add_argument("--max-threshold", help="set the maximal alpha to show. Default to 0.95", type=float, default=0.95)
    return parser.parse_args()


def main():
    args = parse_args()
    logs = load_instance(args.log_file)
    plot_one_figure(logs, args.min_threshold, args.max_threshold)
    if args.title:
        plt.title(args.title)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
