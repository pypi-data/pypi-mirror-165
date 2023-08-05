import json
import setuptools

PACKAGE_NAME = "cgroupy"

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.6',
    description="cgroupy is a python module that provides a simple intrface for managing cgroups",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/morethanunpopular/cgroupy",
    author="Grant Campbell",
    author_email="stars.salvage.man@gmail.com",
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
)
