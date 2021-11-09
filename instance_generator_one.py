from argparse import ArgumentParser
import json

import numpy as np


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "--clients", type=int, help="Number of demand nodes", required=True
    )

    parser.add_argument(
        "--stops", type=int, help="Number of stops nodes", required=True
    )

    parser.add_argument(
        "--min-traffic",
        type=int,
        help="Minimal amount of traffic per facilities per nodes. Default: 1",
        default=1,
    )
    parser.add_argument(
        "--max-traffic",
        type=int,
        help="Maximal amount of traffic per facilities per nodes. Default: 1",
        default=1,
    )

    parser.add_argument(
        "--min-distance",
        type=int,
        help="Minimal distance between a service and a demand node",
        required=True,
    )
    parser.add_argument(
        "--max-distance",
        type=int,
        help="Maximal distance between a service and a demand node",
        required=True,
    )

    parser.add_argument(
        "--instance",
        help="Output instance name. If existing will be overwritten",
        required=True,
    )

    return parser.parse_args()


def random_ndarray(shape, min_val, max_val):
    rnd = np.random.random(shape)
    delta = max_val - min_val
    rnd = rnd * delta
    rnd = rnd + min_val
    return rnd


def save_instance(file_name, lambda_coeff, distances):

    output = {
        "lambda_coeff": lambda_coeff.tolist(),
        "distances": distances.tolist(),
    }

    with open(file_name, "w") as fp:
        json.dump(output, fp)


def main():
    args = parse_args()
    lambda_coeff = random_ndarray(args.stops, args.min_traffic, args.max_traffic)
    distance = random_ndarray(
        (args.clients, args.stops), args.min_distance, args.max_distance
    )
    save_instance(args.instance, lambda_coeff, distance)


if __name__ == "__main__":
    main()
