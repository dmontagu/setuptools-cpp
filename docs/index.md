<p align="center">
  <a href="https://setuptools-cpp.davidmontague.xyz"><img src="https://setuptools-cpp.davidmontague.xyz/img/setuptools-cpp-logo.png" alt="setuptools-cpp"></a>
</p>
<p align="center">
    Simplified packaging for <a href="https://pybind11.readthedocs.io/en/master/">pybind11</a>-based C++ extensions
</p>
<p align="center">
<img src="https://img.shields.io/github/last-commit/dmontagu/setuptools-cpp.svg">
<a href="https://github.com/dmontagu/setuptools-cpp" target="_blank">
    <img src="https://github.com/dmontagu/setuptools-cpp/workflows/build/badge.svg" alt="Build">
</a>
<a href="https://codecov.io/gh/dmontagu/setuptools-cpp" target="_blank">
    <img src="https://codecov.io/gh/dmontagu/setuptools-cpp/branch/master/graph/badge.svg" alt="Coverage">
</a>
<a href="https://app.netlify.com/sites/trusting-archimedes-72b369/deploys">
    <img src="https://img.shields.io/netlify/28b2a077-65b1-4d6c-9dba-13aaf6059877" alt="Netlify status">
</a>
<br />
<a href="https://pypi.org/project/setuptools-cpp" target="_blank">
    <img src="https://badge.fury.io/py/setuptools-cpp.svg" alt="Package version">
</a>
    <img src="https://img.shields.io/pypi/pyversions/setuptools-cpp.svg">
    <img src="https://img.shields.io/github/license/dmontagu/setuptools-cpp.svg">
</p>

---

**Documentation**: <a href="https://setuptools-cpp.davidmontague.xyz" target="_blank">https://setuptools-cpp.davidmontague.xyz</a>

**Source Code**: <a href="https://github.com/dmontagu/setuptools-cpp" target="_blank">https://github.com/dmontagu/setuptools-cpp</a>

---

## Features

* **`Pybind11Extension`**: For standard Pybind11 extensions from C++ source files
* **`CMakeExtension`**: Useful for incorporating CMake-dependent libraries like CGAL
* **Poetry Compatibility**: Easy to use with [poetry](https://python-poetry.org/)'s [custom build system](https://github.com/python-poetry/poetry/issues/11#issuecomment-379484540)


## Basic Usage

You can use the `CMakeExtension` or `Pybind11Extension` classes in your `setup.py` as follows:

```python
from setuptools import setup

from setuptools_cpp import CMakeExtension, ExtensionBuilder, Pybind11Extension

ext_modules = [
    # A basic pybind11 extension in <project_root>/src/ext1:
    Pybind11Extension(
        "my_pkg.ext1", ["src/ext1/ext1.cpp"], include_dirs=["src/ext1/include"]
    ),

    # An extension with a custom <project_root>/src/ext2/CMakeLists.txt:
    CMakeExtension(f"my_pkg.ext2", sourcedir="src/ext2")
]

setup(
    name="my_pkg",
    version="0.1.0",
    packages=["my_pkg"],
    # ... other setup kwargs ...
    ext_modules=ext_modules,
    cmdclass=dict(build_ext=ExtensionBuilder),
    zip_safe=False,
)
```

You can then use standard setuptools commands like `python setup.py install`.

See the [User Guide](https://setuptools-cpp.davidmontague.xyz/user-guide/) for more details.

## Requirements

This package is intended for use with Python 3.6+.

## Installation

```bash
pip install setuptools-cpp
```

## License

This project is licensed under the terms of the MIT license.
