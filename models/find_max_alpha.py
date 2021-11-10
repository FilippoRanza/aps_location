#! /usr/bin/python


from dataclasses import dataclass
from multiprocessing import Pool

from .abstract_model import Model


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
