#! /usr/bin/python



import numpy as np

from models import Model, MyModelOne, ModelConfig, MyModelOneInstance, find_max_alpha_by_facilities
from utils import (
    Log,
    parse_args,
    load_instance,
    compute_reach_coefficent,
    load_json_file,
)




def load_config(file_name):
    config = load_json_file(file_name)
    return config


def main():
    """ """
    args = parse_args()
    instance = load_instance(MyModelOneInstance, args.instance)
    config = load_config(args.config)

    log = Log(args.log_file)
    for conf in config:
        delta_coeff = compute_reach_coefficent(instance.distances, conf)
        model = MyModelOne(instance.lambda_coeff, delta_coeff, args.threads)
        alpha = find_max_alpha_by_facilities(
            model, len(instance.lambda_coeff), args.jobs
        )
        log.add_entry(conf, alpha)

    log.save()


if __name__ == "__main__":
    main()
