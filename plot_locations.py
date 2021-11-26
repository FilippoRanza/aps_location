"""
Plot customer and station map
"""
from argparse import ArgumentParser
from dataclasses import dataclass

import numpy as np
import matplotlib
from matplotlib import pyplot as plt

from utils import load_instance

@dataclass
class Locations:
    clients: np.ndarray
    stops: np.ndarray

def scatter_matrix(values, marker, size):
    x = values[:, 0]
    y = values[:, 1]
    plt.scatter(x, y, marker=marker, s=size)



def parse_args():
    parser = ArgumentParser()
    
    parser.add_argument("locations", help="Specify locations")
    parser.add_argument("--title", help="Set image title")
    parser.add_argument("--file", help="Save image to file")

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
    locs = load_instance(Locations, args.locations)
    size = 35
    scatter_matrix(locs.clients, '.', size)
    scatter_matrix(locs.stops, 's', 3*size)
    plt.legend(['clients', 'stations'])
    if args.title:
        plt.title(args.title)
    
    plt.tight_layout()
    

    if args.file:
        plt.savefig(args.file)
    else:
        plt.show()


if __name__ == '__main__':
    main()


