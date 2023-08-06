import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="SunSip",
    version="1.0.2",
    description="SunSip: Easy Programming Language for Dummies",
    long_description=README,
    long_description_content_type="text/markdown",
    author="NumberBasher",
    author_email="luchang1106@icloud.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["SunSip"],
    include_package_data=True,
    install_requires=['rich'],
    url="https://github.com/TvoozMagnificent/SunSip",
)
