## Poetry

[Poetry](https://python-poetry.org/) is a modern dependency management and packaging tool for use with python libraries. 

Because poetry has its own package building process, it can be difficult to determine how
to package libraries that make use of native extensions or have other install-time logic
that would traditionally be included in the project's `setup.py` file.

The documentation here is based on examples from 
[this github issue](https://github.com/python-poetry/poetry/issues/11#issuecomment-379484540)
describing poetry's custom build system.

## Customizing Poetry's Build Process

To modify the build process, you just need to make a few changes to the `pyproject.toml`, and create a python file
used by poetry to modify its call to `setuptools.setup`.

### `pyproject.toml`
To customize the build process, you need to add the following to your `pyproject.toml`:
* Add the `build` key to the `[tool.poetry]` section of your `pyproject.toml`
    * The value should be the filename of a python file that will contain the custom build keys.
    * Typically, this file is called `build.py` and is placed in the project root. See below for more detail.   

```toml hl_lines="6"
{!./src/poetry_pyproject.toml!}
```

* Add the `[build-system]` section with keys:
    * `build-backend = "poetry.masonry.api"`
    * `requires`, a list containing at least `"poetry>=0.12"`
        * If you use `setuptools-cpp` to build any extensions, you should also add `"setuptools-cpp"` to this list

```toml hl_lines="8 9 10"
{!./src/poetry_pyproject.toml!}
```

### `build.py`
In `pyproject.toml`, we added a reference to a python file to be used by poetry's build process.

This file should define a function called `build`, which accepts a dict containing the keyword arguments that will be
be passed to `setuptools.setup`. The `build` function should then modify this dict in place as appropriate for your
build process.

Here is an example `build.py` that could be used to build native extensions using `setuptools-cpp`:
```python
# build.py

{!./src/poetry_build.py!}
```

To build native extensions, you generally need to add the key `"ext_modules"` with a value that is a list of
subclasses of `setuptools.Extension`. You also need to add `"zip_safe": False` to ensure a platform-specific
wheel is created.

```python hl_lines="20 22"
# build.py

{!./src/poetry_build.py!}
```

!!! tip
    When including native extensions, you may want to build (and publish) prebuilt wheels for your package.

    Otherwise, consumers of your package will need to build from source, which can add challenges
    with related dependencies like CMake, the C++ compiler, pre-installed headers, etc.

    If you publish pre-built wheels, be aware that they are platform-specific and must be built separately for
    each platform you intend to support (e.g., `win`, `macosx`, `manylinux`). 

### `setuptools-cpp` specifics

When using the `Pybind11Extension` or `CMakeExtension` classes provided by `setuptools-cpp`, there are
two changes you need to make beyond the minimum necessary to make use of poetry's masonry build backend:

* As noted above, you need to add `"setuptools-cpp"` to the `build-system.required` key in your `pyproject.toml`
    * This ensures `setuptools-cpp` is installed prior to attempts to build from source

```toml hl_lines="10"
{!./src/poetry_pyproject.toml!}
```

* You also need to specify a custom value for the `cmdclass` argument to `setuptools.setup`: 
```python hl_lines="5 21"
# build.py

{!./src/poetry_build.py!}
```

If you need to further customize the `build_ext` for the `cmdclass` 
(e.g., for compatibility with other types of native extensions),
you can subclass `setuptools_cpp.ExtensionBuilder`, or just copy the relevant parts of its logic.
