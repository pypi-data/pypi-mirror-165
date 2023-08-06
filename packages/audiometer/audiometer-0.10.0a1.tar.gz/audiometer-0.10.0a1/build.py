from typing import Any

from setuptools import Extension


def build(setup_kwargs: dict[str, Any]) -> None:
    setup_kwargs |= {
        "ext_modules": [
            Extension(
                name="audiometer",
                sources=["src/audiometer/main.c"],
                libraries=["m"],
            )
        ],
        "package_data": {
            "audiometer": ["*.pyi", "py.typed"],
        },
    }
