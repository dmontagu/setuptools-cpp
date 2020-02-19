from setuptools import Extension
from setuptools.command.build_ext import build_ext

from setuptools_cpp.cmake_extension import CMakeExtension, build_cmake_extension, prepare_cmake_extensions
from setuptools_cpp.pybind11_extension import prepare_pybind11_extensions


class ExtensionBuilder(build_ext):
    def build_extensions(self) -> None:
        self.prepare_cmake_extensions()
        self.prepare_pybind11_extensions()
        super().build_extensions()

    def build_extension(self, ext: Extension) -> None:
        if isinstance(ext, CMakeExtension):
            self.build_cmake_extension(ext)
        else:
            super().build_extension(ext)

    def prepare_pybind11_extensions(self) -> None:
        dist_version = self.distribution.metadata.get_version()
        prepare_pybind11_extensions(self.extensions, self.compiler, dist_version)

    def prepare_cmake_extensions(self) -> None:
        prepare_cmake_extensions(self.extensions)

    def build_cmake_extension(self, ext: CMakeExtension) -> None:
        ext_full_path = self.get_ext_fullpath(ext.name)
        dist_version = self.distribution.metadata.get_version()
        build_cmake_extension(ext, ext_full_path, dist_version, self.build_temp, self.debug)
