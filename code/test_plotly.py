import argparse
import os
from threading import Thread

import plotly.graph_objects as go
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from viztracer import VizTracer

from fr_selenium import FigureResamplerGUITests
from utils import get_data


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


# --------------------------- create & parse the args ----------------------------------
parser = argparse.ArgumentParser(description="benchmark figure resampler")
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
s = get_data()[: args.n]  # Get the series and reduce to n

# --------------------- start the webdriver
o = Options()
if args.headless:
    o.add_argument('headless')
driver = webdriver.Chrome()
driver.set_page_load_timeout(120)
fr = FigureResamplerGUITests(driver=driver, port=args.port)

# ----------------------------------- VIZTRACER logging --------------------------------
with VizTracer(
        log_gc=False,
        log_async=True,
        output_file=f"{args.save_dir}/plotly__{args.index}__nb_traces={args.nb_traces}__n={args.n}__n_out={args.n_out}__headless={args.headless}.json",
        max_stack_depth=0,
        plugins=["vizplugins.memory_usage"],
) as viz:
    fig = go.Figure()
    [
        fig.add_trace(go.Scattergl(x=s.index, y=s, name=i))
        for i in range(args.nb_traces)
    ]
    viz.add_variable('event', "constructed image")
    
    # t = Thread(target=fig.show_dash, kwargs=dict(mode="external", port=args.port))
    # t.start()
    fig.write_html('tmp.html', include_plotlyjs=True)
    fr.go_to_page("file://" + os.path.abspath("tmp.html"))
    fr.wait_element("xy", wait_time_s=900)
    viz.add_variable('event', "visualization shown")

import time
time.sleep(1)

del fr
os._exit(0)
