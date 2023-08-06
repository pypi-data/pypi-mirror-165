from os import path

from setuptools import find_packages, setup

_dir = path.abspath(path.dirname(__file__))

with open(path.join(_dir, "README.md")) as f:
    long_description = f.read()

project = "mercator/oper/opendap-downloader"
setup(
    name="opendap-downloader",
    version="0.5.0",
    author="Jonathan Brouillet",
    author_email="jbrouillet@mercator-ocean.fr",
    description="Facilitate OPeNDAP download",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://gitlab.mercator-ocean.fr/{project}",
    license="BSD Licence",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    project_urls={
        "Repository": f"https://gitlab.mercator-ocean.fr/{project}",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Environment :: Console",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires=[
        "xarray>=0.21.0",
        "dask>=2022.06.1",
        "netcdf4>=1.5.8",
        "pydap>=3.2.2",
        "requests>=2.26.0",
        "click>=8.0.3",
    ],
    setup_requires=["flake8"],
    python_requires=">=3.8",
)
