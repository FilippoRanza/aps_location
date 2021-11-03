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


@dataclass
class Config:
    radius_small: float
    radius_large: float


def compute_reach_coefficent(distances: np.ndarray, time: float):
    tmp = distances <= time
    return tmp.astype(np.int8)


@dataclass
class Model:
    """
    Build a Gurobi model
    """

    demand: np.ndarray
    config: Config
    distances: np.ndarray
    locations: np.ndarray
    thread_count: int

    def setup(self):
        self.gamma_coeff = compute_reach_coefficent(
            self.distances, self.config.radius_small
        )
        self.delta_coeff = compute_reach_coefficent(
            self.distances, self.config.radius_large
        )
        return self

    def build_model(self, facilities: int, alpha: float, one_sol: False):
        self.model = gp.Model()
        self.add_variables(len(self.locations), len(self.demand))
        self.add_constraints(facilities, alpha)
        self.add_objective()
        if one_sol:
            self.model.setParam("SolutionLimit", 1)
        self.model.setParam("Threads", self.thread_count)

    def try_solve(self):
        self.model.optimize()
        return self.model.status == gp.GRB.OPTIMAL or self.model.status == gp.GRB.SOLUTION_LIMIT

    def add_variables(self, facility_locs: int, demand_locs: int):
        """
        Initialize model variables
        """
        self.aps_count = self.model.addVars(
            range(facility_locs), vtype=gp.GRB.INTEGER, name="y"
        )
        self.k_one_coverage = self.model.addVars(
            range(demand_locs), vtype=gp.GRB.BINARY, name="x_1"
        )
        self.k_two_coverage = self.model.addVars(
            range(demand_locs), vtype=gp.GRB.BINARY, name="x_2"
        )

    def add_constraints(self, facilities: int, alpha: float):
        # constraint (2)
        self.model.addConstrs(
            gp.quicksum(
                self.delta_coeff[i, j] * self.aps_count[j] for j in self.aps_count
            )
            >= 1
            for i, v in enumerate(self.demand)
        )

        # constraint (3)
        self.model.addConstr(
            gp.quicksum(
                d * self.k_one_coverage[x]
                for d, x in zip(self.demand, self.k_one_coverage)
            )
            >= alpha * self.demand.sum()
        )

        # constraint (4)
        self.model.addConstrs(
            gp.quicksum(
                self.gamma_coeff[i, j] * self.aps_count[j] for j in self.aps_count
            )
            >= self.k_one_coverage[x1] + self.k_two_coverage[x2]
            for i, (x1, x2) in enumerate(zip(self.k_one_coverage, self.k_two_coverage))
        )

        # constraint (5)
        self.model.addConstrs(
            x_two <= x_one
            for x_one, x_two in zip(self.k_one_coverage, self.k_two_coverage)
        )

        # constraint (6)
        self.model.addConstr(gp.quicksum(self.aps_count) == facilities)

        # constraint (7)
        self.model.addConstrs(
            self.aps_count[y] <= c for y, c in zip(self.aps_count, self.locations)
        )

    def add_objective(self):
        # Objective function (1)
        self.model.setObjective(
            gp.quicksum(
                d * self.k_two_coverage[k]
                for d, k in zip(self.demand, self.k_two_coverage)
            ),
            gp.GRB.MAXIMIZE,
        )



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
        model.build_model(facilities, alpha, True)
        if model.try_solve():
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
        output = pool.map(cb.callback, range(facility_max_count))

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
    configs = [Config(r1, r2) for r1, r2 in config]
    return configs


@dataclass
class Log:
    file_name: str
    log: list = field(default_factory=list)

    def add_entry(self, conf: Config, alphas):
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
        "--threads", help="specify the number of thread for the backend solver. Default 0, automatic",
        type=int,
        default=0
    )

    parser.add_argument(
        "--jobs", help="specify the number of parallel jobs to run. Default 1",
        type=int,
        default=1
    )

    return parser.parse_args()


def main():
    """ """
    args = parse_args()
    instance = load_instance(args.instance)
    config = load_config(args.config)

    log = Log(args.log_file)
    for conf in config:
        model = Model(
            instance.demand, conf, instance.distances, instance.locations, args.threads
        ).setup()
        alpha = find_max_alpha_by_facilities(model, len(instance.locations), args.jobs)
        log.add_entry(conf, alpha)

    log.save()


if __name__ == "__main__":
    main()
