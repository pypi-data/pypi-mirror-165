

[![](https://codecov.io/gh/nickderobertis/fitbit-downloader/branch/master/graph/badge.svg)](https://codecov.io/gh/nickderobertis/fitbit-downloader)
[![PyPI](https://img.shields.io/pypi/v/fitbit-downloader)](https://pypi.org/project/fitbit-downloader/)
![PyPI - License](https://img.shields.io/pypi/l/fitbit-downloader)
[![Documentation](https://img.shields.io/badge/documentation-pass-green)](https://nickderobertis.github.io/fitbit-downloader/)
![Tests Run on Ubuntu Python Versions](https://img.shields.io/badge/Tests%20Ubuntu%2FPython-3.8%20%7C%203.9%20%7C%203.10-blue)
![Tests Run on Macos Python Versions](https://img.shields.io/badge/Tests%20Macos%2FPython-3.8%20%7C%203.9%20%7C%203.10-blue)
![Tests Run on Windows Python Versions](https://img.shields.io/badge/Tests%20Windows%2FPython-3.8%20%7C%203.9%20%7C%203.10-blue)
[![Github Repo](https://img.shields.io/badge/repo-github-informational)](https://github.com/nickderobertis/fitbit-downloader/)


#  fitbit-downloader

## Overview

A CLI and Python tool for downloading Fitbit data

## Getting Started

Install `fitbit-downloader`:

```
pip install fitbit-downloader
```

A simple example:

```python
import fitbit_downloader

# Do something with fitbit_downloader
```

See a
[more in-depth tutorial here.](
https://nickderobertis.github.io/fitbit-downloader/tutorial.html
)

## Development Status

This project is currently in early-stage development. There may be
breaking changes often. While the major version is 0, minor version
upgrades will often have breaking changes.

## Developing

First, you need a couple global dependencies installed, see their documentation for details:
- [pipx](https://pypa.github.io/pipx/installation/)
- [direnv](https://direnv.net/docs/installation.html)

Then clone the repo and run `npm install` and `mvenv sync dev`. Make your changes and then run `just` to run formatting,
linting, and tests.

Develop documentation by running `just docs` to start up a dev server.

To run tests only, run `just test`. You can pass additional arguments to pytest,
e.g. `just test -k test_something`.

Prior to committing, you can run `just` with no arguments to run all the checks.

### Download Sample Responses

Run `python -m fitbit_downloader.download_samples` to output JSON files 
with the responses.

### Generate Response Models

> Note: There are currently some manual modifications to the generated files. 
> They are all marked with TODO so that we can work them into the generation.
> If you re-run the generation, you will need to manually update the files 
> to make the same changes.

Run `python -m fitbit_downloader.gen_models` to output response models 
in `fitbit_downloader.models` from the sample responses.


## Author

Created by Nick DeRobertis. MIT License.

## Links

See the
[documentation here.](
https://nickderobertis.github.io/fitbit-downloader/
)
