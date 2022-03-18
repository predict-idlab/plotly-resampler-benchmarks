import argparse
import os
import time

import matplotlib.pyplot as plt
from viztracer import VizTracer

from utils import get_data, str2bool

# parse the args
parser = argparse.ArgumentParser(description="benchmark holoviews")
parser.add_argument(
    "--index", required=True, type=int, help="an integer for the accumulator"
)

parser.add_argument(
    "--headless", type=str2bool, default=False,
    help='whether the webdriver is started on a headless manner or not'
)
parser.add_argument("--port", type=int, default=8051, help="the web-app port")
parser.add_argument("--n", type=int, default=1, help="the raw data size")
parser.add_argument(
    "--nb-traces", type=int, default=1, help="The amount of traces to show"
)
parser.add_argument("--n-out", type=int, default=1, help="the aggregated data size")
parser.add_argument(
    "--save-dir",
    type=str,
    default="benchmark_jsons",
    help="whether  the directory in which the benchmark will be saved",
)

args = parser.parse_args()
print(args)

# FILTER WARNINGS
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

s = get_data()[: args.n]  # Get the series and reduce to n
s.index.name = 'timestamp'

# ----------------------------------- VIZTRACER logging --------------------------------
with VizTracer(
        log_gc=False,
        log_async=True,
        output_file=f"{args.save_dir}/matplotlib__{args.index}__nb_traces={args.nb_traces}__n={args.n}__n_out={args.n_out}__headless=False.json",
        max_stack_depth=0,
        plugins=["vizplugins.memory_usage"],
) as viz:
    # The downsampling functionality

    # Graph construction
    fig = plt.figure(figsize=(10, 4))
    viz.add_variable('event', "constructed image")

    plt.ion()
    plt.show()

    for _ in range(args.nb_traces):
        plt.plot(s)
        plt.draw()
        plt.pause(0.0001)
    plt.show(block=False)
    viz.add_variable('event', "visualization shown")

time.sleep(2)
os._exit(0)
