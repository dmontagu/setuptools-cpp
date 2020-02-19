import sys
from distutils.ccompiler import CCompiler
from functools import lru_cache
from typing import Any, List, Tuple

import pybind11
from setuptools import Extension


class Pybind11Extension(Extension):
    def __init__(
        self,
        name: str,
        sources: List[str],
        *args: Any,
        include_dirs: List[str] = None,
        library_dirs: List[str] = None,
        libraries: List[str] = None,
        **kw: Any,
    ):
        pybind_include_dirs = _get_pybind11_include_dirs()
        include_dirs = (include_dirs or []) + pybind_include_dirs
        library_dirs = library_dirs or []
        libraries = libraries or []
        kw.update(dict(include_dirs=include_dirs, library_dirs=library_dirs, libraries=libraries, language="c++",))
        super().__init__(name, sources, *args, **kw)


def prepare_pybind11_extensions(
    extensions: List[Extension], compiler: CCompiler, dist_version: str, extra_opts: List[str] = None,
) -> None:
    pybind11_extensions = [ext for ext in extensions if isinstance(ext, Pybind11Extension)]
    if pybind11_extensions:  # pragma: no branch
        extra_opts = extra_opts or []
        opts, link_opts = _get_pybind11_opts(compiler, dist_version)
        for ext in pybind11_extensions:
            ext.extra_compile_args = opts + extra_opts
            ext.extra_link_args = link_opts


def _get_pybind11_opts(compiler: CCompiler, dist_version: str) -> Tuple[List[str], List[str]]:
    opts = []
    link_opts = []
    compiler_type = getattr(compiler, "compiler_type")  # not necessary, but prevents mypy warnings
    if compiler_type == "unix":
        if sys.platform == "darwin":
            darwin_opts = ["-stdlib=libc++", "-mmacosx-version-min=10.14"]
            opts.extend(darwin_opts)
            link_opts.extend(darwin_opts)
        opts.append(f'-DVERSION_INFO="{dist_version}"')
        opts.append(_get_cpp_flag(compiler))
        if _has_flag(compiler, "-fvisibility=hidden"):
            opts.append("-fvisibility=hidden")
    # TODO: Test on windows
    elif compiler_type == "msvc":  # pragma: no cover
        opts.append(f'/DVERSION_INFO=\\"{dist_version}\\"')
    return opts, link_opts


def _get_cpp_flag(compiler: CCompiler) -> str:
    """Return the -std=c++[11/14/17] compiler flag.
    The newer version is prefered over c++11 (when it is available).
    """
    flags = ["-std=c++17", "-std=c++14", "-std=c++11"]

    for flag in flags:
        if _has_flag(compiler, flag):
            return flag

    raise RuntimeError("Unsupported compiler -- at least C++11 support is needed!")  # pragma: no cover


def _has_flag(compiler: CCompiler, flagname: str) -> bool:
    """
    Return a boolean indicating whether a flag name is supported on the specified compiler.
    """
    import tempfile
    from distutils.errors import CompileError

    extra = ["-stdlib=libc++"] if sys.platform == "darwin" else []

    with tempfile.NamedTemporaryFile("w", suffix=".cpp") as f:
        f.write("int main (int argc, char **argv) { return 0; }")
        try:
            compiler.compile([f.name], extra_postargs=[flagname] + extra)
        except CompileError:
            return False
    return True


@lru_cache()
def _get_pybind11_include_dirs() -> List[str]:
    # Use an lru_cache to prevent multiple searches for directories; maybe unnecessary
    return [pybind11.get_include(user=False), pybind11.get_include(user=True)]
