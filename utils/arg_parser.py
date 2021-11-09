#! /usr/bin/python

from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "instance",
        help="JSON file containing the instance. Loaded values are not validated",
    )
    parser.add_argument(
        "config",
        help="JSON file containing the radius values. Loaded values are not validated",
    )

    parser.add_argument(
        "log_file", help="Specify output log JSON file. If existing will be overwritten"
    )

    parser.add_argument(
        "--threads",
        help="specify the number of thread for the backend solver. Default 0, automatic",
        type=int,
        default=0,
    )

    parser.add_argument(
        "--jobs",
        help="specify the number of parallel jobs to run. Default 1",
        type=int,
        default=1,
    )

    return parser.parse_args()
