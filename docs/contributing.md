## Developing

Once you've cloned the repository, here are some guidelines to set up your environment.

Note that you'll need to be using Python 3.6 or newer,
and you'll need to have [`poetry`](https://python-poetry.org/) installed.  

### Set up the development evironment

After cloning the repository, you can use `poetry` to create a virtual environment: 

```console
$ make develop
```

Behind the scenes, this checks that you have python3 and poetry installed,
then creates a virtual environment and installs the dependencies. At the end, it will print out
the path to the executable in case you want to add it to your IDE.


### Activate the environment

Once the virtual environment is created, you can activate it with:

```console
$ poetry shell
```

To check if this worked, try running: 

```console
$ which python

some/directory/setuptools-cpp-SOMETHING-py3.X/bin/python
```

If the output of this command shows the `python` binary in a path containing `setuptools-cpp` somewhere in the name
(as above), then it worked! 🎉

### Static Code Checks

This project makes use of `black`, `autoflake8`, and `isort` for formatting,
`flake8` for linting, and `mypy` for static type checking.

To auto-format your code, just run:

```console
$ make format
```

It will also auto-sort all your imports, and attempt to remove any unused imports.

You can run flake8 with:

```console
$ make lint
```

and you can run mypy with:

```console
$ make mypy
```

There are a number of other useful makefile recipes; you can see basic documentation of these by calling plain `make`:

```console
$ make
```


## Docs

The documentation uses <a href="https://www.mkdocs.org/" class="external-link" target="_blank">MkDocs</a>.

All the documentation is in Markdown format in the directory `./docs`.

During local development, you can build the site and serve local docs with live-reloading via:

```console
$ make docs-live
```

It will serve the documentation on `http://0.0.0.0:8008`, and you can edit the
 documentation/source files and see the changes in real time.

## Tests

You can run all tests via:

```console
$ make test
```

You can also generate a coverage report with:

```console
make testcov
```

On MacOS, if the tests all pass, the coverage report will be opened directly in a browser; on other operating systems
a link will be printed to the local HTML containing the coverage report.
