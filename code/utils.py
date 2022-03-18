import pandas as pd
import numpy as np
from typing import Union, Tuple
from pathlib import Path
import json
import argparse

n_max = 10_000_000


def get_data() -> pd.Series:
    x = np.arange(n_max)
    y = np.sin(x / 550) + np.random.randn(n_max) / 5
    s = pd.Series(data=y, index=x, name='signal')
    s.index.name = 'timestamp'
    return s


def process_viztrace_json(json_path: Union[str, Path]) -> Tuple[
    pd.DataFrame, pd.DataFrame]:
    with open(json_path, 'r') as f:
        df_viz = pd.json_normalize(json.load(f).get("traceEvents", {}))

    df_mem = df_viz[df_viz.name == 'memory_usage']
    df_mem = df_mem.set_index('ts').sort_index()

    t_start = df_mem.index[0]
    df_mem.index = pd.to_timedelta((df_mem.index - t_start), unit='us')

    df_other = df_viz[df_viz.name != 'memory_usage']
    df_other = df_other.set_index('ts').sort_index()
    df_other.index = pd.to_timedelta((df_other.index - t_start), unit='us')
    df_other = df_other[~df_other.index.isna()]

    df_mem['args.rss'] -= df_mem['args.rss'].min()
    df_mem['args.vms'] -= df_mem['args.vms'].min()

    return df_mem.dropna(axis=1, how='all'), df_other.dropna(axis=1, how='all')


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")
