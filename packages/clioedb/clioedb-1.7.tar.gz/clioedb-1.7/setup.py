import setuptools
from pathlib import Path

setuptools.setup(
    name="clioedb",
    version=1.7,
    description="A module to fetch data from MySQL db as list or save it as text file",
    keywords=["fetch mysql data"],
    long_description=Path("README.md").read_text(),
    author='Cheny Lioe',
    author_email='chenylioe@yahoo.com',
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
