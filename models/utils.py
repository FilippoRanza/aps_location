#! /usr/bin/python


def grb_vars_to_list(grb_vars):
    return [x.x for x in grb_vars.values()]

def grb_vars_to_matrix(grb_vars):
    return [grb_vars_to_list(x) for x in grb_vars]


