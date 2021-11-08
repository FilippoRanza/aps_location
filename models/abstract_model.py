#! /usr/bin/python

import gurobipy as gp


class Model:
    def setup(self):
        return self

    def build_model(self, count: int, alpha: float):
        pass

    def is_fesible(self):
        self.model.setParam("SolutionLimit", 1)
        self.model.optimize()
        return (
            self.model.status == gp.GRB.OPTIMAL
            or self.model.status == gp.GRB.SOLUTION_LIMIT
        )

    def solve(self):
        self.model.optimize()
        return self.model
