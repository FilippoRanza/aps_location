#! /usr/bin/python

""" 
This model is designed to identify 
the best coupling between a customer 
and a facility location. It aims to minimize 
the total distance between each couple of 
customer - facility. 
"""

from dataclasses import dataclass

import gurobipy as gp
import numpy as np

from .abstract_model import Model


@dataclass
class FindBestCoupling(Model):
    distances: np.ndarray
    # delta_coeff: np.ndarray

    def build_model(self):
        customers, stops = self.distances.shape
        self.model = gp.Model()
        self.add_variables(customers, stops)
        self.add_constraints(customers, stops)
        self.add_objective_function(customers, stops)

    def add_variables(self, customers: int, stops: int):
        self.coupling = np.empty((customers, stops), dtype=np.object)
        for i in range(customers):
            for j in range(stops):
                var = self.model.addVar(vtype=gp.GRB.BINARY, name=f"x_{i}-{j}")
                self.coupling[i, j] = var
        self.model.update()

    def add_constraints(self, customers: int, stops: int):

        # constraint 1
        for i in range(customers):
            self.model.addConstr(gp.quicksum(self.coupling[i, :]) == 1)

        # constraint 2
        gamma = get_gamma_param(customers, stops)
        for j in range(stops):
            self.model.addConstr(gp.quicksum(self.coupling[:, j]) <= gamma * customers)

    def add_objective_function(self, customers: int, stops: int):
        self.model.setObjective(
            gp.quicksum(
                self.coupling[i, j] * self.distances[i, j]
                for i in range(customers)
                for j in range(stops)
            ),
            gp.GRB.MINIMIZE,
        )


def get_gamma_param(customer: int, stops: int):
    tmp = customer / stops
    tmp = np.ceil(tmp)
    return tmp
