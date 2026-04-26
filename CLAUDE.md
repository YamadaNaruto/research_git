# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a research project for empirically analyzing the relationship between **test smells** and **code smells** (maintainability) across the git history of target repositories. Scripts extract file versions at each commit, run static analysis tools, and aggregate results into CSV files for further analysis.

## External Tool Dependencies

The scripts depend on two external tools that must be installed separately:

- **PyNose** — test smell detector: `python3 /Users/yamadanaruto/Downloads/PyNose-ASE2022/runner.py`
- **SonarScanner** — code smell / maintainability detector: `sonar-scanner` CLI (must be in PATH)

PyNose writes JSON output to `/Users/yamadanaruto/Desktop/pynose_output2/`.

## Running Scripts

All scripts are run from the **target repository's root** (i.e., `cd` into the repo being analyzed before running), not from this repo's root. Git commands inside the scripts use the CWD to resolve file paths.

```bash
# Collect test smells for all files in a folder
python3 /path/to/src/collect_testsmels.py

# Collect test smells for a single file
python3 /path/to/src/collect_testsmels_onlyfile.py

# Collect code smells (SonarQube) for a single file
python3 /path/to/src/collect_codesmells.py

# Convert PyNose JSON outputs to aggregated CSV
python3 /path/to/src/get_csv_stats.py

# Merge test smell + code smell data by date into aggregated.csv
python3 /path/to/src/collect_csv.py
```

## Architecture and Data Flow

```
Target Repo (git)
      |
      | git log → commit hashes + timestamps
      v
collect_testsmels.py / collect_testsmels_onlyfile.py
      |
      | writes each commit's file content to temp dir
      | runs PyNose on each version
      v
pynose_output2/ (JSON results per commit)
      |
get_csv_stats.py
      | parses JSON → per-file CSV + aggregated.csv (one row per commit)
      | columns: date, test_file_count, test_case_count, test_method_count, <smell_names>, total
      v
aggregated.csv  (test smell counts over time)

collect_codesmells.py
      | writes each commit's file to temp dir
      | runs sonar-scanner
      v
SonarQube DB  (maintainability scores)

collect_csv.py
      | merges test smell totals + maintainability scores by date
      | (merge-by-time algorithm: advances whichever series has the earlier next event)
      v
aggregated.csv  (date, testsmells, codesmells)
```

## Key Implementation Details

- **Hardcoded paths** throughout the scripts (target repo path, PyNose path, temp dirs). These must be changed per machine and per repository being analyzed.
- `collect_testsmels.py` exports three reusable functions (`get_hashes_of_file`, `get_commit_time`, `get_content_file_at_commit`) that `collect_codesmells.py` imports.
- `get_csv_stats.py` uses `dataclasses-json` to deserialize PyNose's camelCase JSON output into Python dataclasses. It handles both list-root and dict-root JSON formats from PyNose.
- `collect_csv.py` uses an event-merge algorithm (similar to merge-sort merge) to interleave two time series (test smells and code smells) and carry forward the latest known value for each series.
- `tpot/` is a cloned external repository (TPOT AutoML) used as a target for analysis — it is not part of this project's source code.

## Python Dependencies

```bash
pip install pandas dataclasses-json
```
