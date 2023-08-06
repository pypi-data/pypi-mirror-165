import os
from setuptools import setup, find_packages

with open("requirements.txt", "r") as file:
    requirements = [line for line in file.read().splitlines() if line]

with open(os.path.join("src", "rhdzmota", "VERSION"), "r") as file:
    version = file.read().strip()

with open("README.md") as file:
    readme = file.read()

setup(
    name="rhdzmota",
    version=version,
    description="RHDZMOTA Package",
    long_description=readme,
    long_description_content_type='text/markdown',
    url="https://github.com/rhdzmota/rhdzmota-package",
    author="Rodrigo H. Mota",
    author_email="contact@rhdzmota.com",
    packages=find_packages(where="src"),
    package_dir={
        "": "src"
    },
    scripts=[
        "bin/rhdzmota"
    ],
    install_requires=requirements,
    include_package_data=True,
)
