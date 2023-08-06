# File with defaults for ease of use
from pathlib import PosixPath
from typing import Union

import h5py


def exparams_from_meta(meta: Union[dict, PosixPath, str], extras=["ph"]):
    """
    Obtain parameters from metadata of hdf5 file
    """
    meta = meta if isinstance(meta, dict) else load_attributes(meta)
    base = {
        "tree": {"general": {"None": ["area", "volume", "eccentricity"]}},
        "multichannel_ops": {},
    }

    av_channels = {
        "Citrine",
        "GFP",
        "GFPFast",
        "mCherry",
        "pHluorin405",
        "Flavin",
        "Cy5",
        "mKO2",
    }

    default_reductions = {"np_max"}
    default_metrics = {
        "mean",
        "median",
        "imBackground",
        "background_max5",
        "max2p5pc",
        "max2p5pc_med",
        "max5px",
        "max5px_med",
        # "nuc_est_conv",
    }

    default_rm = {r: default_metrics for r in default_reductions}
    # default_rm["None"] = ["nuc_conv_3d"]

    av_flch = av_channels.intersection(meta["channels/channel"]).difference(
        {"Brightfield", "DIC", "BrightfieldGFP"}
    )

    for ch in av_flch:
        base["tree"][ch] = default_rm

    base["sub_bg"] = av_flch

    # Additional extraction defaults when channels available
    if "ph" in extras:
        if {"pHluorin405", "GFPFast"}.issubset(av_flch):

            sets = {
                b + a: (x, y)
                for a, x in zip(
                    ["", "_bgsub"],
                    (
                        ["GFPFast", "pHluorin405"],
                        ["GFPFast_bgsub", "pHluorin405_bgsub"],
                    ),
                )
                for b, y in zip(["em_ratio", "gsum"], ["div0", "np_add"])
            }
            for i, v in sets.items():
                base["multichannel_ops"][i] = [
                    *v,
                    default_rm,
                ]

    return base


def load_attributes(file: str, group="/"):
    with h5py.File(file, "r") as f:
        meta = dict(f[group].attrs.items())
    return meta
