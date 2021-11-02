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

    def setup(self):
        self.gamma_coeff = compute_reach_coefficent(
            self.distances, self.config.radius_small
        )
        self.delta_coeff = compute_reach_coefficent(
            self.distances, self.config.radius_large
        )
        return self

    def build_model(self, facilities: int, alpha: float):
        self.model = gp.Model()
        self.add_variables(len(self.locations), len(self.demand))
        self.add_constraints(facilities, alpha)
        self.add_objective()

    def try_solve(self):
        self.model.optimize()
        return self.model.status == gp.GRB.OPTIMAL

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
        model.build_model(facilities, alpha)
        if model.try_solve():
            min_alpha = alpha
        else:
            max_alpha = alpha
    return alpha


def find_max_alpha_by_facilities(model: Model, facility_max_count: int):
    """
    Find the maximal alpha value depending on the number of facilities.
    Tries with any possible facility count from 1 to facility_max_count
    """
    return [find_max_alpha(model, f + 1) for f in range(facility_max_count)]


def main():
    """
    Script's main function.
    Now it just contains some
    random values to see if the
    model compiles
    """
    demand = np.array([1, 2, 3])
    config = Config(10, 20)
    distances = np.array([[13, 21], [7, 8], [17, 10]])
    locations = np.array([2, 2])
    model = Model(demand, config, distances, locations).setup()
    alpha = find_max_alpha_by_facilities(model, len(locations))
    print(alpha)


if __name__ == "__main__":
    main()
