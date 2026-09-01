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
3. Clone the repository, run `cd eterna100-benchmarking`, `git lfs install` and `git lfs pull`
3. Install python dependencies via `pip install -r requirements.txt`
4. Prep external libraries with `setup_external.sh`

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

## How to run the Vienna1 and Vienna2 engines
Each benchmark is defined by a **stock build of a specific ViennaRNA version**, run with no flags
other than the temperature. This is all `scripts/util/fold.py` does:

```
RNAfold -T 37.0
```

| Benchmark | Engine | Energy parameters | `dangles` default |
|---|---|---|--:|
| **Eterna100-V1** ("Vienna 1") | ViennaRNA **1.8.5** | Turner 1999 | **1** |
| **Eterna100-V2** ("Vienna 2") | ViennaRNA **2.1.9** or **2.6.4** | Turner 2004 | **2** |

The `dangles` defaults are compiled in, not passed on the command line: `lib/fold_vars.c` in 1.8.5
and 2.1.9, `src/ViennaRNA/model.h` in 2.6.4. Eterna's in-game engine is the Vienna 1 model (EternaJS sets `EPars.DANGLES = 1`) and early design methods like NEMO used this model (e.g., `nemo.cpp` loads `vrna185x.par` with `dangles = 1`).

2.1.9 and 2.6.4 return identical MFE structures for Eterna100 designs, so either may be used for
Vienna 2.


### Common pitfall: Turner 1999 parameters alone are not Vienna 1

Loading the Turner 1999 parameters into a ViennaRNA 2.x binary or its Python bindings does **not**
reproduce Vienna 1, because 2.x leaves `dangles` at 2 while 1.8.5 uses 1. The result is a hybrid of
the two models that is neither benchmark, and on Eterna100 targets it is more permissive than
either: it accepts designs that neither stock engine folds to the target.

```python
import RNA

# WRONG for Vienna 1 -- dangles is still 2
RNA.params_load_RNA_Turner1999()
structure, mfe = RNA.fold_compound(seq).mfe()

# The Vienna 1 model, inside ViennaRNA 2.x
RNA.params_load_RNA_Turner1999()
md = RNA.md(dangles=1)
structure, mfe = RNA.fold_compound(seq, md).mfe()
```

From command line, `RNAfold -P rna_turner1999.par -d1` on 2.1.9 or 2.6.4 reproduces the 1.8.5 energy model
exactly, but **not** the traceback to derive the MFE structure. Where the MFE structure is **degenerate**, Vienna 2.x can pick a different co-optimal structure than 1.8.5 does. So, score against the stock 1.8.5 binary for Vienna 1 benchmark – for degenerate MFEs no parameter-file substitution with 2.x binaries reproduces it.

