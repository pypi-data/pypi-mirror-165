import codecs
import os
from setuptools import find_packages, setup
from pathlib import Path

this_directory = Path(__file__).parent

PACKAGE_NAME = "machineop"
VERSION = "0.0.2"
AUTHOR = "LiveByTheCode (Archer EarthX)"
AUTHOR_EMAIL = "archerearthx@gmail.com"
DESCRIPTION = "The domain specific language for operating statemachines. The default machine included in the package is microwave oven."
LONG_DESCRIPTION = (this_directory / "README.md").read_text()
KEYWORDS = "textX DSL python domain specific languages state machines"
LICENSE = "MIT"

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    keywords=KEYWORDS,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True,
    package_data={"": ["*.tx","*.pymo"]},
    install_requires=["argparse","textx","textx_ls_core"],
    entry_points={
        "textx_languages": ["MachineOp = machine_operator:state_machine_lang"],
        "console_scripts": ["machineop = machine_operator:operate"]
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires='>=3.7'
)