"""
The code is licensed under the MIT license.
"""

from os import path
from setuptools import setup, find_packages

# Content of the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md")) as f:
    long_description = f.read()

# Setup
setup(
    name="pulire",
    version="0.0.3",
    author="Meteostat",
    author_email="info@meteostat.net",
    description="A lightweight DataFrame validation library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/meteostat/pulire",
    keywords=["timeseries"],
    python_requires=">=3.6.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pandas", "numpy"],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Database",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
)
