# pyMetricCli

pyMetricCli is a collection of scripts and API implementations for generating and playing with metrics.

[![License](https://img.shields.io/badge/license-bsd-3.svg)](https://choosealicense.com/licenses/bsd-3-clause/) [![Repo Status](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip) [![CI](https://github.com/NewTec-GmbH/pyMetricCli/actions/workflows/ci.yml/badge.svg)](https://github.com/NewTec-GmbH/pyMetricCli/actions/workflows/ci.yml)

- [Installation](#installation)
- [Overview](#overview)
- [Usage](#usage)
- [Examples](#examples)
- [Used Libraries](#used-libraries)
- [Issues, Ideas And Bugs](#issues-ideas-and-bugs)
- [License](#license)
- [Contribution](#contribution)

## Installation

```cmd
git clone https://github.com/NewTec-GmbH/pyMetricCli.git
cd pyMetricCli
pip install .
```

This will also install the latest version of [pyJiraCli](https://github.com/NewTec-GmbH/pyJiraCli), [pyPolarionCli](https://github.com/NewTec-GmbH/pyPolarionCli), and [pySupersetCli](https://github.com/NewTec-GmbH/pySupersetCli) in your Python environment.

## Overview

pyMetricCli requires an adapter file to be supplied by the user. This shall contain the credentials and result-handling logic for the seach results. Please **DO NOT** commit this file into any public repository as your credentials might be exposed.

An example adapter can be found [here](examples/adapter/adapter.py).

## Usage

Show help information:

```cmd
pyJiraCli --help
```

Usage:

```cmd
usage: pyMetricCli [-h] -a <adapter_file> [--version] [-v]

Collection of scripts and API implementations for generating and playing with metrics.

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v, --verbose         Print full command details before executing the command. Enables logs of type INFO and WARNING.

required arguments:
  -a <adapter_file>, --adapter_file <adapter_file>
                        Adapter file to be used.
```

Example:

```cmd
pyJiraCli --verbose --adapter_file "examples\adapter\adapter.py"
```

### Adapter

The adapter file must contain the `Adapter` Class derived from the `AdapterInterface`, including all the methods and members defined in the interface.

The `***_config` dictionaries must be filled with the user credentials for each service. The `output` dictionary defines the columns of the table that will be sent to Superset, and this cannot be changed after the first time the script is ran. If you are receiving an Error 422 from Superset, a change in this dictionary may be the reason and you should contact your administrator so resolve the issue.

## Examples

Check out the [Examples](./examples) in the corresponding folder.

## Used Libraries

Used 3rd party libraries which are not part of the standard Python package:

- [toml](https://github.com/uiri/toml) - Parsing [TOML](https://en.wikipedia.org/wiki/TOML) - MIT License
- [pyJiraCli](https://github.com/NewTec-GmbH/pyJiraCli) - Interfacing with Jira - BSD-3 License
- [pyPolarionCli](https://github.com/NewTec-GmbH/pyPolarionCli) - Interfacing with Polarion - BSD-3 License
- [pySupersetCli](https://github.com/NewTec-GmbH/pySupersetCli) - Interfacing with Superset - BSD-3 License

## Issues, Ideas And Bugs

If you have further ideas or you found some bugs, great! Create an [issue](https://github.com/NewTec-GmbH/pyMetricCli/issues) or if you are able and willing to fix it by yourself, clone the repository and create a pull request.

## License

The whole source code is published under [BSD-3-Clause](https://github.com/NewTec-GmbH/pyMetricCli/blob/main/LICENSE).
Consider the different licenses of the used third party libraries too!

## Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, shall be licensed as above, without any additional terms or conditions.
