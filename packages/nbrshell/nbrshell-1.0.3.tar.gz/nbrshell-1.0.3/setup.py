from setuptools import setup

# read the contents of README file from ./nbrshell/README.md
#
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.rst").read_text(encoding='utf-8')

setup(
    name="nbrshell",
    version="1.0.3",
    description='Jupyter Notebook "cell magic" functions to remotely execute shell script typed in a notebook cell.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author="A.Balbekov",
    author_email="albert.y.balbekov@gmail.com",
    packages=["nbrshell"], # same as name
    install_requires=["paramiko"],    # external packages
    license="BSD License",
    url="https://github.com/abalbekov/nbrshell",
    keywords=['remote shell script execution']
)
