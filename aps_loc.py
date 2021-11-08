#! /usr/bin/python

"""
Implement the Double Coverage Problem
with the model describe in:
    'Solving an Ambulance Location Model by Tabu Search' 
        by Gendreau, Laporte and Semet.
In this script the problem is solved exactly using Gurobi.
"""

from argparse import ArgumentParser
import json
from dataclasses import dataclass, field
from multiprocessing import Pool

import numpy as np
import gurobipy as gp

from models import Model, GendreauLaporteSemetModel, ModelConfig





def find_max_alpha(model: Model, facilities: int, tol=1e-6):
    """
    Search among possible alpha values
    to find the maximal value that allow the
    given instance to be feasible with the given number
    of facilities.
    The value is searched using binary search.
    """
    min_alpha = 0.0
    max_alpha = 1.0
    while abs(min_alpha - max_alpha) > tol:
        alpha = (max_alpha + min_alpha) / 2
        model.build_model(facilities, alpha)
        if model.is_fesible():
            min_alpha = alpha
        else:
            max_alpha = alpha
    return alpha


@dataclass
class PoolCallback:
    model: Model

    def callback(self, i):
        return find_max_alpha(self.model, i)


def find_max_alpha_by_facilities(model: Model, facility_max_count: int, jobs: int):
    """
    Find the maximal alpha value depending on the number of facilities.
    Tries with any possible facility count from 1 to facility_max_count
    """

    cb = PoolCallback(model)
    with Pool(jobs) as pool:
        output = pool.map(cb.callback, range(facility_max_count), chunksize=1)

    return list(output)


@dataclass
class Instance:
    demand: np.ndarray
    distances: np.ndarray
    locations: np.ndarray


def to_ndarray(json_dict, name):
    value = json_dict[name]
    return np.array(value)


def load_json_file(file_name):
    with open(file_name) as file:
        data = json.load(file)
    return data


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


@dataclass
class Log:
    file_name: str
    log: list = field(default_factory=list)

    def add_entry(self, conf, alphas):
        conf = (conf.radius_small, conf.radius_large)
        self.log.append((conf, alphas))

    def save(self):
        with open(self.file_name, "w") as fp:
            json.dump(self.log, fp)


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
