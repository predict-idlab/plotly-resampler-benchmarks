# plotly-resampler benchmarks

## <p align="center"> <a href="https://predict-idlab.github.io/plotly-resampler/"><img alt="tsflex" src="https://raw.githubusercontent.com/predict-idlab/plotly-resampler/main/docs/sphinx/_static/logo.png" height="100"></a></p>

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?color=black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?)](http://makeapullrequest.com) 

This repository withholds the [benchmark results](reports/benchmark_fig.png) and visualization code of the `plotly-resampler` paper and [toolkit](https://github.com/predict-idlab/plotly-resampler).

![bencmark_result](reports/benchmark_fig.png)


## Flow

The benchmark process follows these steps for each visualization-configuration:

1. Each toolkit-visualization configuration script is called 10 times to average out the memory usage and runtime. Remark that by re-calling the script in separate runs, no caching or memory is shared among executions.
2. Script execution:
   1. Construct the synthetic visualization data
   2. [VizTracer](https://github.com/gaogaotiantian/viztracer) starts logging
   3. Construct the visualization according to the configuration
   4. Wait till the graph is rendered in a selenium browser.
   5. VizTracer stops logging
   6. Write the VizTracer results to a JSON-file

The existing [benchmark JSONs](code/benchmark_jsons/) were collected on a desktop with an *AMD Ryzen 5 2600x @3.8Ghz* CPU and *48GB* RAM, with *Arch Linux* as operating system. Other running processes were limited to a minimum.

> more information about these outcomes can be found in the [**reports**](reports/README.md) readme.

## Instructions

To install the required dependencies, just run:

```bash
poetry install
```

If you want to **re-run the benchmarks**, use the [run_scripts](code/run_scripts.ipynb) notebook to generate new benchmark JSONs and then visualize them with the [benchmark visualization](code/benchmark_visualizations.ipynb) notebook.

## Contributing

We are open to new-benchmark use-cases via **pull-requests**!<br>

> Examples of other interesting benchmarks are
>  * other data properties
>  * other eligible tools
>  * benchmarking graph-interaction response time.

<br>

---
<p align="center">
👤 <i>Jonas Van Der Donckt</i>
</p>
