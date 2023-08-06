import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / 'README.md').read_text()

# This call to setup() does all the work
setup(
    name="easyspex",
    version="0.0.1",
    author="Zefang Shen",
    author_email="zefang2455@gmail.com",
    description="Utilities for spectroscopic pre-processing, modelling, and evaluations.",
    long_description=README,
    long_description_content_type="text/markdown",
    # url="https://github.com/zefang-shen/easyspex.git",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["easyspex"],
    install_requires=[
        'numpy',
        'pandas',
    ],
    include_package_data=True,
    zip_safe=True,
    # entry_points={}
)
