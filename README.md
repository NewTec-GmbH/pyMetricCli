# NewTec Python Template

---

- In GitHub, use the button `Use this template` to create a new repository.
- Clone the repository, and open `.vscode\template_python.code-workspace` to open the workspace with Visual Studio Code (VSCode).
- Install the recommended extensions if desired.
- Search and replace the keyword `template_python` with the name of your project `<your_project_name>`.
- Change the name in the workspace file `.vscode\template_python.code-workspace` to `.vscode\<your_project_name>.code-workspace`. You may need to restart VSCode.
- Change the name in the src folder `src\template_python` to `src\<your_project_name>`
- Change the imports in the `__main__.py` file if required:

```python
from <your_project_name>.version import __version__, __author__, __email__, __repository__, __license__
from <your_project_name>.ret import Ret
```

- Change the author, email and description in `pyproject.toml` and `setup.cfg`.
- Delete this block when you are done.

---

[![License](https://img.shields.io/badge/license-bsd-3.svg)](https://choosealicense.com/licenses/bsd-3-clause/) [![Repo Status](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip) [![CI](https://github.com/NewTec-GmbH/template_python/actions/workflows/ci.yml/badge.svg)](https://github.com/NewTec-GmbH/template_python/actions/workflows/ci.yml)

- [Installation](#installation)
- [Overview](#overview)
- [Usage](#usage)
- [Commands](#commands)
- [Examples](#examples)
- [Used Libraries](#used-libraries)
- [Issues, Ideas And Bugs](#issues-ideas-and-bugs)
- [License](#license)
- [Contribution](#contribution)

## Installation

WIP

## Overview

WIP

## Usage

WIP

## Commands

WIP

## Examples

Check out the all the [Examples](./examples).

## Used Libraries

Used 3rd party libraries which are not part of the standard Python package:

- [toml](https://github.com/uiri/toml) - Parsing [TOML](https://en.wikipedia.org/wiki/TOML) - MIT License

## Issues, Ideas And Bugs

If you have further ideas or you found some bugs, great! Create an [issue](https://github.com/NewTec-GmbH/template_python/issues) or if you are able and willing to fix it by yourself, clone the repository and create a pull request.

## License

The whole source code is published under [BSD-3-Clause](https://github.com/NewTec-GmbH/template_python/blob/main/LICENSE).
Consider the different licenses of the used third party libraries too!

## Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, shall be licensed as above, without any additional terms or conditions.
