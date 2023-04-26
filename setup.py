"""A setuptools based setup module.

Run using:
    $ python -m pip install <flags> .

Most used flags:
    -e, --editable <path/url>
        Install a project in editable mode (i.e. setuptools “develop mode”)
        from a local project path or a VCS url.

    -v, --verbose
        Give more output.
"""
# pylint: disable=invalid-name

from pathlib import Path
from setuptools import setup, find_packages

here = Path(__file__).parent.absolute()  # pylint: disable=no-member

# Get the long description from the README file
with open(here / "README.md", encoding="utf-8") as f:
    long_description = f.read()

with open(here / "requirements.txt", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="dasqa",
    version="0.1",
    description="MQT Designer for Alternative Superconducting Quantum Architectures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cda-tum/mqt-dasqa",
    author="Jagatheesan Kunasaikaran",
    author_email="jagatheesan.kunasaikaran@tum.de",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
    ],
    keywords="quantum sdk hardware eda",
    packages=find_packages(),
    package_data={"dasqa": []},
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "dasqa=src.__main__:main",
        ],
    },
    project_urls={
        "Bug Tracker": "https://github.com/cda-tum/issues",
        "Documentation": "https://github.com/cda-tum/mqt-dasqa",
        "Source Code": "https://github.com/cda-tum/mqt-dasqa",
    },
)
