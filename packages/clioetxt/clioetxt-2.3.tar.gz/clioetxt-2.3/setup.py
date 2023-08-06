import setuptools
from pathlib import Path

setuptools.setup(
    name="clioetxt",
    version=2.3,
    description="A module to extract, transform (search, invert, format) and load text file or csv file",
    keywords=["txt file", "csv file"],
    long_description=Path("README.md").read_text(),
    author='Cheny Lioe',
    author_email='chenylioe@yahoo.com',
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
