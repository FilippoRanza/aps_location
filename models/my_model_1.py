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
class MyModelOneInstance:
    lambda_coeff: np.ndarray
    distances: np.ndarray



@dataclass
class MyModelOne(Model):

    lambda_coeff: np.ndarray
    delta_coeff: np.ndarray
    threads: int

    def get_vars(self):
        return self.facility_vars, self.customer_facility_assign_vars

    def build_model(self, aps_count: int, alpha: float):
        self.model = gp.Model()
        self.setup_variables()
        self.setup_contraints(aps_count, alpha, self.delta_coeff)
        self.setup_objective_function(self.lambda_coeff)

    def setup_variables(self):
        cust_count, loc_count = self.delta_coeff.shape
        self.facility_vars = self.model.addVars(
            range(loc_count), vtype=gp.GRB.BINARY, name="y"
        )
        self.customer_vars = self.model.addVars(
            range(cust_count), vtype=gp.GRB.BINARY, name="z"
        )

        self.customer_facility_assign_vars = [
            self.model.addVars(
                range(loc_count),
                vtype=gp.GRB.BINARY,
                name=f"x_{j}",
            )
            for j in range(cust_count)
        ]
        self.model.update()

    def setup_contraints(self, aps_count: int, alpha: float, delta_coeff: np.ndarray):
        cust_count, loc_count = self.delta_coeff.shape

        # constrain 1
        self.model.addConstr(gp.quicksum(self.facility_vars) == aps_count)

        # constrain 2

        self.model.addConstrs(
            self.customer_vars[i]
            <= gp.quicksum(self.customer_facility_assign_vars[i].values())
            for i in range(cust_count)
        )

        self.model.addConstr(
            gp.quicksum(self.customer_vars.values()) >= alpha * len(self.customer_vars)
        )

        # constrain 4
        self.model.addConstrs(
            self.customer_facility_assign_vars[i][j]
            <= delta_coeff[i, j] * self.facility_vars[j]
            for i in range(cust_count)
            for j in range(loc_count)
        )

    def setup_objective_function(self, coeff: np.ndarray):
        self.model.setObjective(
            gp.quicksum(
                l * self.facility_vars[y] for l, y in zip(coeff, self.facility_vars)
            ),
            gp.GRB.MAXIMIZE,
        )
