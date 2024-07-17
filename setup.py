from __future__ import print_function
import os
import sys
import platform
from setuptools import setup, find_packages


def read(fname):
    """Utility function to read the README file."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def package_files(directory, extension="yaml"):
    paths = []
    for path, directories, filenames in os.walk(directory):
        for filename in filenames:
            if filename.split(".")[-1] == extension:
                paths.append(os.path.join("..", path, filename))

    return paths


def dir_this_file():
    return os.path.dirname(os.path.realpath(__file__))


bcutils_dir = os.path.join(dir_this_file(), "bcutils")
bcutils_yaml_files = package_files(bcutils_dir, "yaml")

provided_dir = os.path.join(dir_this_file(), "systems", "provided")
provided_yaml_files = package_files(provided_dir, "yaml")

sample_dir = os.path.join(dir_this_file(), "sample")
sample_yaml_files = package_files(bcutils_dir, "yaml")


package_data = {
    "": bcutils_yaml_files
    + sample_yaml_files
}

print(package_data)

setup(
    name="bc-utils",
    version="0.1.6",
    author="Robert Carver",
    description=(
        "Python utility automation scripts for Barchart.com"
        " (https://github.com/bug-or-feature/bc-utils)"
    ),
    license="GNU GPL v3",
    keywords="Python Barchat.com automation",
    url="https://github.com/bug-or-feature/bc-utils",
    packages=find_packages(),
    package_data=package_data,
    long_description=read("README.md"),
    install_requires=[
        "pandas",
        "pytz",
        "PyYAML",
        "requests",
        "beautifulsoup4",
        "pytest",
        "Flask",
        "Werkzeug",
        "statsmodels",
        "PyPDF2",
    ],
    tests_require=["nose", "flake8"],
    extras_require=dict(),
    test_suite="nose.collector",
    include_package_data=True,
)
