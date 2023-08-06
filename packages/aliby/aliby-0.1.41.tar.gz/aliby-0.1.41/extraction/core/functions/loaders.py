from inspect import getfullargspec, getmembers, isfunction

import numpy as np

from extraction.core.functions import cell, trap
from extraction.core.functions.custom import localisation
from extraction.core.functions.distributors import trap_apply
from extraction.core.functions.math_utils import div0


def load_cellfuns_core():
    # Generate str -> trap_function dict from functions in core.cell
    return {
        f[0]: f[1]
        for f in getmembers(cell)
        if isfunction(f[1])
        and f[1].__module__.startswith("extraction.core.functions")
    }


def load_custom_args():
    """
    Load custom functions. If they have extra arguments (starting at index 2,
    after mask and image) also load these.
    """
    funs = {
        f[0]: f[1]
        for f in getmembers(localisation)
        if isfunction(f[1])
        and f[1].__module__.startswith("extraction.core.functions")
    }
    args = {
        k: getfullargspec(v).args[2:]
        for k, v in funs.items()
        if set(["cell_mask", "trap_image"]).intersection(
            getfullargspec(v).args
        )
    }

    return (
        {k: funs[k] for k in args.keys()},
        {k: v for k, v in args.items() if v},
    )


def load_cellfuns():
    """
    Input:

    Returns:
       Dict(str, function)
    """
    # Generate str -> trap_function dict from core.cell and core.trap functions
    cell_funs = load_cellfuns_core()
    CELLFUNS = {}
    for k, f in cell_funs.items():
        if isfunction(f):

            def tmp(f):
                args = getfullargspec(f).args
                if len(args) == 1:
                    return lambda m, _: trap_apply(f, m)
                else:
                    return lambda m, img: trap_apply(f, m, img)

            CELLFUNS[k] = tmp(f)
    return CELLFUNS


def load_trapfuns():
    """
    Load functions that are applied to an entire trap (or tile, or subsection of a given image),
    instead of being applied to single cells.
    """
    TRAPFUNS = {
        f[0]: f[1]
        for f in getmembers(trap)
        if isfunction(f[1])
        and f[1].__module__.startswith("extraction.core.functions")
    }
    return TRAPFUNS


def load_funs():
    """
    Combine all automatically-loaded functions
    """
    CELLFUNS = load_cellfuns()
    TRAPFUNS = load_trapfuns()

    return CELLFUNS, TRAPFUNS, {**TRAPFUNS, **CELLFUNS}


def load_redfuns():  # TODO make defining reduction functions more flexible
    """
    Load z-stack reduction functions.
    """
    RED_FUNS = {
        "np_max": np.maximum,
        "np_mean": np.mean,
        "np_median": np.median,
        "None": None,
    }
    return RED_FUNS


def load_mergefuns():
    """
    Load functions to merge multiple channels
    """
    MERGE_FUNS = {"div0": div0, "np_add": np.add}
    return MERGE_FUNS
