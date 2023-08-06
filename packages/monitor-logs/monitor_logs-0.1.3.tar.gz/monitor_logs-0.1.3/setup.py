##setup.py

import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "monitor_logs/README.md").read_text()

# This call to setup() does all the work
setup(name = 'monitor_logs', 
    version = '0.1.3', 
    description = 'Monitor your logs from anywhere', 
    long_description=README,
    long_description_content_type="text/markdown",
    packages = ['monitor_logs'], 
    url="https://github.com/Vinithavn/Monitor-model-logs/",
    zip_safe = False
)