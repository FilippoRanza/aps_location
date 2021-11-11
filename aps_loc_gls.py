#! /usr/bin/python

"""
Implement the Double Coverage Problem
with the model describe in:
    'Solving an Ambulance Location Model by Tabu Search' 
        by Gendreau, Laporte and Semet.
In this script the problem is solved exactly using Gurobi.
"""

from dataclasses import dataclass

import numpy as np

from models import (
    Model,
    GendreauLaporteSemetModel,
    ModelConfig,
    find_max_alpha_by_facilities,
)
from utils import (
    Log,
    parse_args,
    load_instance,
    load_json_file,
)


@dataclass
class Instance:
    demand: np.ndarray
    distances: np.ndarray
    locations: np.ndarray


def load_config(file_name):
    config = load_json_file(file_name)
    configs = [ModelConfig(r1, r2) for r1, r2 in config]
    return configs


def main():
    """ """
    args = parse_args()
    instance = load_instance(Instance, args.instance)
    config = load_config(args.config)

    log = Log(args.log_file)
    for conf in config:
        model = GendreauLaporteSemetModel(
            instance.demand, conf, instance.distances, instance.locations, args.threads
        ).setup()
        alpha = find_max_alpha_by_facilities(model, len(instance.locations), args.jobs)
        log.add_entry((conf.radius_small, conf.radius_large), alpha)

    log.save()


if __name__ == "__main__":
    main()
