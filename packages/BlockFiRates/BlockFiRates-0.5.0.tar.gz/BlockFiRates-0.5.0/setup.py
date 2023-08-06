from pathlib import Path
from setuptools import setup, find_packages

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

requirements = ["cloudscraper==1.2.60"]

setup_requirements = ["pytest-runner"]

tests_requirements = ["pytest==7.1.2"]

dev_requirements = [
    "build==0.8.0",
    "pre-commit==2.19.0",
    "setuptools==62.3.4",
    "twine==4.0.1",
] + tests_requirements

extras_requirements = {"dev": dev_requirements}

setup(
    author="P. G. Ó'Slatara",
    author_email="pgoslatara@gmail.com",
    classifiers=[
        "Environment :: Console",
        "Framework :: Flake8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords=["crypto", "python3", "blockfi"],
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="BlockFiRates",
    packages=find_packages(include=["blockfirates", "blockfirates.*"]),
    python_requires=">=3.7.*,<=3.10.*",
    url="https://github.com/pgoslatara/blockfirates",
    version="0.5.0",
    install_requires=requirements,
    setup_requires=setup_requirements,
    tests_require=tests_requirements,
    extras_require=extras_requirements,
)
