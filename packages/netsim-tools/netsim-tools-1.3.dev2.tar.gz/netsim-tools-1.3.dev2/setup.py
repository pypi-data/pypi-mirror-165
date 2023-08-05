""" redirect netsim-tools to networklab """
import sys
from setuptools import setup, find_packages

sys.path.append('..')
from netsim import __version__

setup(
  name="netsim-tools",
  version=__version__,
  packages=[],
  author="Ivan Pepelnjak",
  author_email="ip@ipspace.net",
  description="CLI-based Virtual Networking Lab Abstraction Layer",
  install_requires=["networklab"],
  classifiers=[
    "Topic :: Utilities",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Operating System :: POSIX :: Linux",
    "Operating System :: MacOS",
  ],
  url="https://github.com/ipspace/netsim-tools",
  python_requires='>=3.7',  # Due to e.g. 'capture_output' in subprocess.run
)
