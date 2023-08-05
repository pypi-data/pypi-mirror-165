import json
import setuptools

PACKAGE_NAME = "cgroupy"
setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.5',
    description="cgroupy is a python module that provides a simple intrface for managing cgroups",
    url="https://github.com/morethanunpopular/cgroupy",
    author="Grant Campbell",
    author_email="stars.salvage.man@gmail.com",
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
)
