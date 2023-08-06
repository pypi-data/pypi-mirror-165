from typing import Any

from Cython.Build import cythonize
from Cython.Distutils.build_ext import new_build_ext
from setuptools import Extension


def build(setup_kwargs: dict[str, Any]) -> None:
    setup_kwargs |= {
        "ext_modules": cythonize(
            module_list=[
                Extension(
                    name="audiometer",
                    sources=["src/audiometer/main.pyx"],
                    libraries=["m"],
                )
            ],
            compiler_directives={
                "language_level": "3",
                "always_allow_keywords": True,
            },
        ),
        "package_data": {
            "audiometer": ["*.pyi", "py.typed"],
        },
        "cmdclass": {"build_ext": new_build_ext},
    }
