#! /usr/bin/python

""" 
This file contains the gurobipy implementation
of my model.
"""
from dataclasses import dataclass

import numpy as np
import gurobipy as gp

from .abstract_model import Model


@dataclass
class MyModelOne(Model):

    lambda_coeff: np.ndarray
    delta_coeff: np.ndarray
    threads: int

    def build_model(self, aps_count: int, alpha: float):
        self.model = gp.Model()
        self.setup_variables(*self.delta_coeff.size)
        self.setup_contraints(aps_count, alpha, self.delta_coeff)
        self.setup_objective_function(self.lambda_coeff)

    def setup_variables(self, cust_count: int, loc_count: int):
        self.facility_vars = self.model.addVars(
            range(loc_count), vtype=gp.GRB.BINARY, name="y"
        )
        self.customer_vars = self.model.addVars(
            range(cust_count), vtype=gp.GRB.BINARY, name="z"
        )

        self.customer_facility_assign_vars = [
            self.model.addVars(
                ((i, j) for i in range(cust_count)),
                vtype=gp.GRB.BINARY,
                name="x",
            )
            for j in range(loc_count)
        ]

    def setup_contraints(self, aps_count: int, alpha: float, delta_coeff: np.ndarray):
        # constrain 1
        self.model.addConstr(gp.quicksum(self.facility_vars) == aps_count)

        # constrain 2
        self.model.addConstrs(
            z <= gp.quicksum(x_row)
            for z, x_row in zip(self.customer_vars, self.customer_facility_assign_vars)
        )

        # constrain 3
        self.model.addConstr(
            gp.quicksum(self.customer_vars) >= alpha * len(self.customer_vars)
        )

        # constrain 4
        self.model.addConstrs(
            self.customer_facility_assign_vars[x] <= d * y
            for x, d in zip(x_row, d_row)
            for x_row, d_row, y in zip(
                self.customer_facility_assign_vars, delta_coeff, self.facility_vars
            )
        )

    def setup_objective_function(self, coeff: np.ndarray):
        self.model.setObjective(
            gp.quicksum(
                l * self.facility_vars[y] for l, y in zip(coeff, self.facility_vars)
            ),
            gp.GRB.MAXIMIZE,
        )
