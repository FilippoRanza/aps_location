#! /usr/bin/python

""" 
Random instance generator for
aps_loc.py. Generate only the instances
and not config file.
"""


from argparse import ArgumentParser
import json

import numpy as np


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "--demand", type=int, help="Number of demand nodes", required=True
    )
    parser.add_argument(
        "--min-demand",
        type=int,
        help="Minimal value of demand per nodes. Default: 1",
        default=1,
    )
    parser.add_argument(
        "--max-demand",
        type=int,
        help="Maximal value of demand per nodes. Default: 5",
        default=5,
    )

    parser.add_argument(
        "--facility", type=int, help="Number of facility nodes", required=True
    )
    parser.add_argument(
        "--min-facility",
        type=int,
        help="Minimal number of facilities per nodes. Default: 1",
        default=1,
    )
    parser.add_argument(
        "--max-facility",
        type=int,
        help="Maximal number of facilities per nodes. Default: 1",
        default=1,
    )

    parser.add_argument(
        "--min-distance",
        type=int,
        help="Minimal distance between a service and a demand node",
        required=True,
    )
    parser.add_argument(
        "--max-distance",
        type=int,
        help="Maximal distance between a service and a demand node",
        required=True,
    )

    parser.add_argument(
        "--instance",
        help="Output instance name. If existing will be overwritten",
        required=True
    )

    return parser.parse_args()


def random_ndarray(shape, min_val, max_val):
    rnd = np.random.random(shape)
    delta = max_val - min_val
    rnd = rnd * delta
    rnd = rnd + min_val
    return rnd

def save_instance(file_name, demand, locations, distance):

    output = {
        "demand": demand.tolist(),
        "locations": locations.tolist(),
        "distances": distance.tolist()
    }

    with open(file_name, "w") as fp:
        json.dump(output, fp)

def main():
    args = parse_args()
    demand = random_ndarray(args.demand, args.min_demand, args.max_demand)
    locations = random_ndarray(args.facility, args.min_facility, args.max_facility)
    distance = random_ndarray((args.demand, args.facility), args.min_distance, args.max_distance)
    save_instance(args.instance, demand, locations, distance)



if __name__ == "__main__":
    main()
