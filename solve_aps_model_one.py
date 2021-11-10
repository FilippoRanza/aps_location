#! /usr/bin/python

"""
Solve Model 1 exactly with a given 
instance configuration.
"""
from argparse import ArgumentParser
import json


from models import MyModelOne, MyModelOneInstance
from models.utils import grb_vars_to_list, grb_vars_to_matrix
from utils import load_instance, compute_reach_coefficent, export_results




def solve(distance, lambda_coeff, delta_coeff, alpha, aps_count):
    model = MyModelOne(distance, lambda_coeff, delta_coeff, 0)
    model.build_model(aps_count, alpha)
    model.solve()
    y_vars, x_vars = model.get_vars()
    y_vars = grb_vars_to_list(y_vars)
    x_vars = grb_vars_to_matrix(x_vars)
    return y_vars, x_vars


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("instance", help="specify JSON instance file")
    parser.add_argument("alpha", help="set alpha parameter. Value in range [0, 1]", type=float)
    parser.add_argument("radius", help="set delta radius", type=int)
    parser.add_argument("aps_count", help="set number of APSs", type=int)
    
    return parser.parse_args()

def main():
    args = parse_args()
    instance = load_instance(MyModelOneInstance, args.instance)
    delta_coeff = compute_reach_coefficent(instance.distances, args.radius)
    y, x = solve(instance.distances, instance.lambda_coeff, delta_coeff, args.alpha, args.aps_count)
    export_results("results-new.json", y=y, x=x)

if __name__ == '__main__':
    main()
