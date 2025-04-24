# Eterna100 Benchmarking

[![Paper](https://img.shields.io/badge/paper-bioRxiv-a82525)](https://www.biorxiv.org/content/10.1101/2021.08.26.457839v2)


Scripts and results for benchmarking RNA design algorithms with the Eterna100-V1 and Eterna100-V2 benchmarks

## Setup
1. System Prequisites:
  * Unix environment (tested on Linux, other operating systems may require alternate processes for setting up external dependencies)
  * An available CUDA device, Turing generation or earlier (for retraining Eternabrain if GPU acceleration is desired)
2. Ensure the following prerequisites are installed:
  * git and git-lfs
  * Python 3.11+
  * make, gcc, and g++ (tested with gcc10 and gcc14 - C++17 language feature support is required) for retriving and compiling external dependencies (along with git)
  * Anaconda/miniconda (for isolated environments and python installations necessary for each algorithm)
  * CUDA 10.0 and cuDNN 7.6 (for retraining Eternabrain if GPU acceleration is desired)
3. Install python dependencies via pip install -r requirements.txt
4. Prep external libraries with setup_external.sh

Note that setup_external.sh will by default configure the trained models in `retrained-models` to be available.
If you want to train the models yourself, you should set the environment variable `EBENCH_SKIP_PRETRAINED=1`
to ensure the pipeline only uses the newly-trained models from `scripts/queue_train.py`

## Organization

`data/eterna100_puzzles.tsv`: Metadata for the Eterna100-V1 and Eterna100-V2 benchmarks

`data/results.tsv`: Benchmarking results

`external/`: External dependencies

`scripts/algorithms`: Modules for benchmarking individual algorithms

`scripts/util`: Utility modules

`scripts/benchmark.py`: Script to run an algorithm benchmarks in a single configuration

`scripts/queue_benchmarks.py`: Script to run algorithm benchmarks in bulk

`scripts/queue_train.py`: Script to run retraining for machine learning models

`scripts/stats.py`: Summarize benchmark results

## Usage

* To retrain machine learning models, run run `scripts/queue_train.py` (By default trains all models and runs sequentially - run `queue_train.py -h` for full usage information)
* To benchmark an algorithm in a particular configuration, run `scripts/benchmark.py` (Run `benchmark.py -h` for full usage information)
* To run benchmarks in bulk, run `scripts/queue_benchmarks.py` (By default runs all benchmarks and runs sequentially - run `queue_benchmarks.py -h` for full usage information)
* To generate summary statistics, run `scripts/stats.py`
