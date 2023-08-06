import sys
from pathlib import Path

from setuptools import setup, find_packages

IBLPYBPOD_CURRENT_VERSION = "1.8.2a2"
CURRENT_DIRECTORY = Path(__file__).parent.absolute()
CURRENT_PYTHON_VERSION = sys.version_info[:2]
REQUIRED_PYTHON_VERSION = (3, 8)
VER_ERR_MSG = """
==========================
Unsupported Python version
==========================
This version of iblutil requires Python {}.{}, but you're trying to
install it on Python {}.{}.
"""
if CURRENT_PYTHON_VERSION < REQUIRED_PYTHON_VERSION:
    sys.stderr.write(VER_ERR_MSG.format(*REQUIRED_PYTHON_VERSION + CURRENT_PYTHON_VERSION))
    sys.exit(1)

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    require = [x.strip() for x in f.readlines() if not x.startswith('git+')]

# def read(rel_path):
#     here = Path(__file__).parent.absolute()
#     with open(here.joinpath(rel_path), "r") as fp:
#         return fp.read()
#
#
# def get_version(rel_path):
#     for line in read(rel_path).splitlines():
#         if line.startswith("__version__"):
#             delim = '"' if '"' in line else "'"
#             return line.split(delim)[1]
#     else:
#         raise RuntimeError("Unable to find version string.")
# package_finder_list = [
#     ""
# ]

setup(
    name='iblpybpod',
    # version=get_version(Path("iblpybpod").joinpath("__init__.py")),
    version=IBLPYBPOD_CURRENT_VERSION,
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON_VERSION),
    description='IBL implementation of pybpod software',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='IBL Staff',
    url='https://github.com/int-brain-lab/iblpybpod/',
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=['scratch', 'tests']),  # same as name
    include_package_data=True,
    install_requires=require,
    # entry_points={"console_scripts": ["start-pybpod=base.pybpodgui_plugin.__main__:start"]},
    entry_points={"console_scripts": ["start-pybpod=pybpodgui_plugin.__main__:start"]},
    # entry_points={"console_scripts": ["start-pybpod=base.pybpod-gui-plugin.test:main"]},
    scripts=[]
)
