#! /usr/bin/python

"""
Solve the best coupling model
"""
from argparse import ArgumentParser


from models import FindBestCoupling
from utils import compute_reach_coefficent, load_json_file, to_ndarray


def parse_args():
    parser = ArgumentParser()

    parser.add_argument("distances", help="set distance file")
    # parser.add_argument("radius", help="set max accetable distance", type=int)

    return parser.parse_args()


def main():
    args = parse_args()
    data = load_json_file(args.distances)
    distances = to_ndarray(data, "distances")
    # delta_coeff = compute_reach_coefficent(distances, args.radius)

    model = FindBestCoupling(distances)
    model.build_model()
    model.solve()


if __name__ == "__main__":
    main()
