#! /usr/bin/python

"""
Implement the Double Coverage Problem
with the model describe in:
    'Solving an Ambulance Location Model by Tabu Search' 
        by Gendreau, Laporte and Semet.
In this script the problem is solved exactly using Gurobi.
"""

from argparse import ArgumentParser
from dataclasses import dataclass

import numpy as np

from models import Model, GendreauLaporteSemetModel, ModelConfig
from utils import find_max_alpha_by_facilities, Log, load_json_file, to_ndarray


@dataclass
class Instance:
    demand: np.ndarray
    distances: np.ndarray
    locations: np.ndarray


def load_instance(file_name):
    instance = load_json_file(file_name)
    demand = to_ndarray(instance, "demand")
    distances = to_ndarray(instance, "distances")
    locations = to_ndarray(instance, "locations")

    return Instance(demand, distances, locations)


def load_config(file_name):
    config = load_json_file(file_name)
    configs = [ModelConfig(r1, r2) for r1, r2 in config]
    return configs


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "instance",
        help="JSON file containing the instance. Loaded values are not validated",
    )
    parser.add_argument(
        "config",
        help="JSON file containing the radius values. Loaded values are not validated",
    )

    parser.add_argument(
        "log_file", help="Specify output log JSON file. If existing will be overwritten"
    )

    parser.add_argument(
        "--threads",
        help="specify the number of thread for the backend solver. Default 0, automatic",
        type=int,
        default=0,
    )

    parser.add_argument(
        "--jobs",
        help="specify the number of parallel jobs to run. Default 1",
        type=int,
        default=1,
    )

    return parser.parse_args()


def main():
    """ """
    args = parse_args()
    instance = load_instance(args.instance)
    config = load_config(args.config)

    log = Log(args.log_file)
    for conf in config:
        model = GendreauLaporteSemetModel(
            instance.demand, conf, instance.distances, instance.locations, args.threads
        ).setup()
        alpha = find_max_alpha_by_facilities(model, len(instance.locations), args.jobs)
        log.add_entry(conf, alpha)

    log.save()


if __name__ == "__main__":
    main()
