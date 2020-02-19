from setuptools import setup

from setuptools_cpp import CMakeExtension, ExtensionBuilder, Pybind11Extension

ext_modules = [
    # A basic pybind11 extension in <project_root>/src/ext1:
    Pybind11Extension(
        "my_pkg.ext1", ["src/ext1/ext1.cpp"], include_dirs=["src/ext1/include"]
    ),
    # An extension with a custom <project_root>/src/ext2/CMakeLists.txt:
    CMakeExtension(f"my_pkg.ext2", sourcedir="src/ext2"),
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
