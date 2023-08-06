import os
from pathlib import Path
from setuptools import setup
from pip._internal.req import parse_requirements


this_directory = Path(__file__).parent
package_directory = 'mssqlgenerator'
description_file = (this_directory / package_directory / "README.md")
requirements_file = (this_directory / package_directory / "requirements.txt")

long_description = None
if os.path.exists(description_file):
    # read the contents of README file
    long_description = description_file.read_text()

install_requires = None
if os.path.exists(requirements_file):
    # read the contents of requirements file
    reqs = parse_requirements(requirements_file, session="test")
    install_requires = [str(ir.req) for ir in reqs]

# call setup to generate distributable
setup(
    name="mssqlgenerator",
    version="1.1.1-1",
    author="Kamil Javed",
    author_email="kamiljaved98@gmail.com",
    url="https://github.com/kamiljaved/mssqlgenerator",
    packages=["mssqlgenerator"],
    description="Simple T-SQL query generator based on JSON parameters.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.8.10',
    install_requires=install_requires,
)
