import importlib.util
import os
import shutil
import sys
from pathlib import Path
from typing import Iterator, List

import pytest
from _pytest.monkeypatch import MonkeyPatch
from setuptools import setup

from setuptools_cpp import CMakeExtension, ExtensionBuilder, Pybind11Extension, __version__

TESTS_DIR = Path(__file__).parent
PACKAGE_NAME = "test_pkg"


@pytest.fixture
def install_environment(monkeypatch: MonkeyPatch) -> None:
    sys_path = list(sys.path)
    sys_path.insert(0, str(TESTS_DIR))
    monkeypatch.setattr(sys, "path", sys_path)
    monkeypatch.setattr(sys, "argv", [__file__, "build_ext", "--inplace"])


@pytest.fixture(scope="session", autouse=True)
def install_paths() -> Iterator[None]:
    os.chdir(TESTS_DIR)

    # Create package directory
    test_pkg_dirs = [TESTS_DIR / PACKAGE_NAME / name for name in ["pybind11", "cmake"]]
    for test_pkg_dir in test_pkg_dirs:
        test_pkg_dir.mkdir(parents=True, exist_ok=True)

    yield
    for egg_path in TESTS_DIR.iterdir():
        if egg_path.name.endswith("egg-info"):
            shutil.rmtree(str(egg_path))

    # Clean up build files
    for folder in ["build", "dist", "var", PACKAGE_NAME]:
        folder_path = TESTS_DIR / folder
        if folder_path.exists():
            shutil.rmtree(str(folder_path))


def get_pybind_modules(package_name: str) -> List[Pybind11Extension]:
    return [
        Pybind11Extension(f"{package_name}.pybind11.compiled", ["cpp/src/test_pkg.cpp"], include_dirs=["cpp/include"],)
    ]


def get_cmake_modules(package_name: str) -> List[CMakeExtension]:
    return [CMakeExtension(f"{package_name}.cmake.compiled", sourcedir="cpp")]


def prepare_installed_module(name: str) -> None:
    for file in (TESTS_DIR / "test_pkg" / name).iterdir():
        if file.name.endswith(".so"):
            spec = importlib.util.spec_from_file_location(f"test_pkg.{name}.compiled", file)
            importlib.util.module_from_spec(spec)


def test_install_pybind11(install_environment: None) -> None:
    setup(
        name=PACKAGE_NAME,
        version=__version__,
        ext_modules=[*get_pybind_modules(PACKAGE_NAME)],
        packages=[PACKAGE_NAME],
        cmdclass=dict(build_ext=ExtensionBuilder),
        zip_safe=False,
    )

    prepare_installed_module("pybind11")
    from test_pkg.pybind11.compiled import add as pybind_add

    assert pybind_add(1, 1) == 2


def test_install_cmake(install_environment: None) -> None:
    setup(
        name=PACKAGE_NAME,
        version=__version__,
        ext_modules=[*get_cmake_modules(PACKAGE_NAME)],
        packages=[PACKAGE_NAME],
        cmdclass=dict(build_ext=ExtensionBuilder),
        zip_safe=False,
    )

    prepare_installed_module("cmake")
    from test_pkg.cmake.compiled import add as cmake_add

    assert cmake_add(1, 1) == 2
