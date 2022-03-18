import argparse
import os

import holoviews as hv
import numpy as np
import panel as pn
from plotly_resampler.downsamplers import LTTB
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from viztracer import VizTracer

from fr_selenium import FigureResamplerGUITests
from utils import get_data, str2bool

# --------------------------- create & parse the args ----------------------------------
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

# ------------------ FILTER WARNINGS
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# --------------------- Get the series and reduce to n
s = get_data()[: args.n]

# --------------------- start the webdriver
o = Options()
if args.headless:
    o.add_argument('headless')
fr = FigureResamplerGUITests(driver=webdriver.Chrome(), port=args.port)
hv.extension('bokeh')

# ----------------------------------- VIZTRACER logging --------------------------------
with VizTracer(
        log_gc=False,
        log_async=True,
        output_file=f"{args.save_dir}/holoviews_LTTB__{args.index}__nb_traces={args.nb_traces}__n={args.n}__n_out={args.n_out}__headless={args.headless}.json",
        max_stack_depth=0,
        plugins=["vizplugins.memory_usage"],
) as viz:
    # define The downsampling functionality
    lttb = LTTB()


    def resample_lttb(x_range) -> hv.Curve:
        if x_range is None or (np.isnan(x_range[0]) or np.isnan(x_range[1])):
            s_ = s
        else:
            s_ = s[int(x_range[0]): int(x_range[1])]
        return hv.Curve(
            lttb.downsample(s_, n_out=args.n_out).reset_index(), "timestamp"
        )


    # Graph construction
    layout = hv.Overlay([
        hv.DynamicMap(
            resample_lttb,
            streams=[hv.streams.RangeX()],
        )
        for _ in range(args.nb_traces)
    ]).collate()
    layout.opts(hv.opts.Curve(axiswise=True, width=800, height=500))
    viz.add_variable('event', "constructed image")

    # serve the graph
    server = pn.serve(layout, show=False, port=args.port, threaded=True)

    fr.go_to_page()
    fr.wait_element("bk-tool-icon-wheel-zoom", wait_time_s=600)
    viz.add_variable('event', "visualization shown")

del fr
os._exit(0)
