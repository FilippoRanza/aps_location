#! /usr/bin/python

"""
Solve Model 1 exactly with a given 
instance configuration.
"""
from argparse import ArgumentParser


from models import MyModelOne, MyModelOneInstance
from utils import load_instance, compute_reach_coefficent


def solve(lambda_coeff, delta_coeff, alpha, aps_count):
    model = MyModelOne(lambda_coeff, delta_coeff, 0)
    model.build_model(aps_count, alpha)
    model.solve()


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("instance", help="specify JSON instance file")
    parser.add_argument("alpha", help="set alpha parameter. Value in range [0, 1]", type=float)
    parser.add_argument("radius", help="set delta radius", type=int)
    parser.add_argument("aps-count", help="set number of APSs", type=int)
    
    return parser.parse_args()

def main():
    args = parse_args()
    instance = load_instance(MyModelOneInstance, parser.instance)
    delta_coeff = compute_reach_coefficent(instance.distances, args.radius)
    solve(instance.lambda_coeff, delta_coeff, args.alpha, args.aps_count)

if __name__ == '__main__':
    main()
