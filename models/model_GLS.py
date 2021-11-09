#! /usr/bin/python

""" 
A gurobipy implementation of the model 
described in:
    'Solving an Ambulance Location Model by Tabu Search' 
        by Gendreau, Laporte and Semet.

"""

from .abstract_model import Model
from dataclasses import dataclass, field

import numpy as np
import gurobipy as gp

from utils import compute_reach_coefficent


@dataclass
class ModelConfig:
    radius_small: float
    radius_large: float


@dataclass
class GendreauLaporteSemetModel(Model):
    """
    Build a Gurobi model
    """

    demand: np.ndarray
    config: ModelConfig
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

    def build_model(self, facilities: int, alpha: float):
        self.model = gp.Model()
        self.add_variables(len(self.locations), len(self.demand))
        self.add_constraints(facilities, alpha)
        self.add_objective()
        self.model.setParam("Threads", self.thread_count)

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
