# coding: utf-8
import os

"""
    Deci Training Toolkit
"""

from setuptools import setup
from setuptools import find_packages

README_LOCATION = "README.md"
REQ_LOCATION = "requirements.txt"
REQ_PRO_LOCATION = "requirements.pro.txt"
VERSION_FILE = "version.txt"
INIT_FILE = "src/super_gradients/__init__.py"

PACKAGE_NAME = 'super-gradients-taranis'

def readme():
    """print long description"""
    with open(README_LOCATION, encoding="utf-8") as f:
        return f.read()


def get_requirements():
    with open(REQ_LOCATION, encoding="utf-8") as f:
        requirements = f.read().splitlines()
        return [r for r in requirements if not r.startswith("--") and not r.startswith("#")]


def get_pro_requirements():
    with open(REQ_PRO_LOCATION, encoding="utf-8") as f:
        return f.read().splitlines()


def _version(package_name):
    fname = f"src/super_gradients/version.py"
    with open(fname, 'r') as f:
        ver_str = f.read()


    if all(env_var in os.environ for env_var in ['AGROBRAIN_COMMON_CONFIGURATION', 'BRANCH_NAME', 'BUILD_NUMBER']):
        ver_str = _get_version_from_server(package_name, ver_str)
        with open(fname, 'w') as f:
            f.write(ver_str)

    return ver_str


def _get_version_from_server(package_name, ver_str):
    import requests
    url = f"{os.environ['AGROBRAIN_COMMON_CONFIGURATION']}/deploy_tools/packages/get_next_version"
    major = int(ver_str.split('.')[0])
    minor = int(ver_str.split('.')[1])

    params = {"package_name": package_name,
              "branch_name": os.environ['BRANCH_NAME'],
              "build_number": os.environ['BUILD_NUMBER'],
              "major": major,
              "minor": minor}
    headers = {'accept': 'application/json'}

    response = requests.get(url, params=params, headers=headers, timeout=30)

    if response.status_code != 200:
        raise RuntimeError(
            f"Failed to get next version from packages manager. Status code: {response.status_code}. Response: {response.text}")

    print(f"Got next version: {response.json()}")
    return response.json()


setup(
    name=PACKAGE_NAME,
    version=_version(PACKAGE_NAME),
    description="SuperGradients",
    author="Deci AI",
    author_email="rnd@deci.ai",
    url="https://docs.deci.ai/super-gradients/documentation/source/welcome.html",
    keywords=["Deci", "AI", "Training", "Deep Learning", "Computer Vision", "PyTorch", "SOTA", "Recipes", "Pre Trained", "Models"],
    install_requires=get_requirements(),
    packages=find_packages(where="./src"),
    package_dir={"": "src"},
    package_data={
        "super_gradients.recipes": ["*.yaml", "**/*.yaml"],
        "super_gradients.common": ["auto_logging/auto_logging_conf.json"],
        "super_gradients.examples": ["*.ipynb", "**/*.ipynb"],
        "super_gradients": ["requirements.txt", "requirements.pro.txt"],
    },
    long_description=readme(),
    long_description_content_type="text/markdown",
    extras_require={"pro": get_pro_requirements()},
)
