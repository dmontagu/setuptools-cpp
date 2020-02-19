import os
import platform
import re
import subprocess
import sys
import sysconfig
from distutils.version import LooseVersion
from pathlib import Path
from typing import List

from setuptools import Extension


class CMakeExtension(Extension):
    def __init__(self, name: str, sourcedir: str = "") -> None:
        super().__init__(name, sources=[])
        self.sourcedir = str(Path(sourcedir).resolve())


def prepare_cmake_extensions(extensions: List[Extension]) -> None:
    cmake_extensions = [x for x in extensions if isinstance(x, CMakeExtension)]
    if cmake_extensions:  # pragma: no branch
        try:
            out = subprocess.check_output(["cmake", "--version"])
        except OSError:  # pragma: no cover
            raise RuntimeError(
                "CMake must be installed to build the following extensions: "
                + ", ".join(e.name for e in cmake_extensions)
            )
        # TODO: Add Windows test coverage
        if platform.system() == "Windows":  # pragma: no cover
            cmake_version = LooseVersion(re.search(r"version\s*([\d.]+)", out.decode()).group(1))  # type: ignore
            if cmake_version < "3.1.0":
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")


def build_cmake_extension(
    ext: CMakeExtension, ext_full_path: str, dist_version: str, build_temp: str, debug: bool,
) -> None:
    extdir = Path(ext_full_path).parent.resolve()
    cmake_args = [
        f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}",
        f"-DPYTHON_EXECUTABLE={sys.executable}",
    ]

    cfg = "Debug" if debug else "Release"
    build_args = ["--config", cfg]

    # TODO: Add Windows test coverage
    if platform.system() == "Windows":  # pragma: no cover
        cmake_args += ["-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}".format(cfg.upper(), extdir)]
        if sys.maxsize > 2 ** 32:
            cmake_args += ["-A", "x64"]
        build_args += ["--", "/m"]
    else:
        cmake_args += ["-DCMAKE_BUILD_TYPE=" + cfg]
        build_args += ["--", "-j4"]
    cmake_args += ["-DPYTHON_INCLUDE_DIR={}".format(sysconfig.get_path("include"))]

    env = os.environ.copy()
    env["CXXFLAGS"] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get("CXXFLAGS", ""), dist_version)
    Path(build_temp).mkdir(parents=True, exist_ok=True)
    subprocess.check_call(["cmake", ext.sourcedir] + cmake_args, cwd=build_temp, env=env)
    subprocess.check_call(["cmake", "--build", "."] + build_args, cwd=build_temp)
