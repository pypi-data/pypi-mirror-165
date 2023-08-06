# -*- coding: utf-8 -*-

import os

from setuptools import setup
from sphinx_harumaru_themes import themes


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        if os.path.basename(os.path.normpath(path)) == "__pycache__":
            continue
        for filename in filenames:
            paths.append(os.path.join("..", path, filename))
    return paths

with open("README.rst") as f:
    readme = f.read()

setup(
    name="sphinx_harumaru_themes",
    version="0.5",
    author="DanielSDVG",
    author_email="danielsdvg@gmail.com",
    url="",
    description="A package with cute Sphinx documentation themes",
    long_description=readme,
    license="MIT",
    packages=["sphinx_harumaru_themes"],
    package_data={
        "sphinx_harumaru_themes": package_files("sphinx_harumaru_themes")
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "sphinx.html_themes":
            [f"{t} = sphinx_harumaru_themes" for t in themes]
    },
)