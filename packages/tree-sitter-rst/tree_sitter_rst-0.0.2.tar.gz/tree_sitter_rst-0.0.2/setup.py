import pathlib
import re
import setuptools


from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
from setuptools.command.build_ext import build_ext
from setuptools import Extension, setup
from tree_sitter import Language, Parser
from pathlib import Path




class BuildExtCommand(build_ext):
    """Ensure built extensions are added to the correct path in the wheel."""


    def build_extension(self, ext):
        fp  = self.get_ext_fullpath(ext.name)
        Language.build_library(
            # Store the library in the `build` directory
            fp,
            # Include one or more languages
            [
                "tree-sitter-rst",
            ],
        )
        pass


setuptools.setup(
    name="tree_sitter_rst",
    ext_modules=[
        Extension(
            name="tree_sitter_rst.rst",  # as it would be imported
                               # may include packages/namespaces separated by `.`

            sources=["rst.source"], # all sources are compiled into a single binary file
        ),
    ],
    version="0.0.2",
    description="Binary Python wheels for tree_sitter_rst parser.",
    long_description="",
    author="Matthias Bussonnier",
    author_email="bussonniermatthias@gmail.com",
    zip_safe=False,
    url="",
    license="BSD",
    packages=["tree_sitter_rst"],
    package_data={"tree_sitter_rst": ["rst.so"]},
    install_requires=["tree-sitter"],
    cmdclass={
        "build_ext": BuildExtCommand,
    },
)
