from setuptools import setup, find_packages
from pathlib import Path

this_dir = Path(__file__).parent
long_disc = (this_dir / "README.md").read_text()

setup(
    name="pysimrel-pkg-therimalaya", # Replace with your own username
    version="0.6.2",
    author="Raju Rimal",
    author_email="therimalaya@gmail.com",
    description="Simulation of Linear Model Data",
    long_description=long_disc,
    long_description_content_type="text/markdown",
    url="https://github.com/simulatr/pysimrel",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
