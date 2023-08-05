import pathlib
from setuptools import setup, find_packages

from pykv import __version__

long_description = (pathlib.Path(__file__).parent.resolve() / "README.md").read_text(
    encoding="utf-8"
)

setup(
    name="pykv",
    version=__version__,
    author="skyline93",
    author_email="glf9832@163.com",
    url="https://github.com/skyline93/pykv",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    description="A key-value storage in the memory, it is simple and fast.",
    long_description=long_description, 
)
