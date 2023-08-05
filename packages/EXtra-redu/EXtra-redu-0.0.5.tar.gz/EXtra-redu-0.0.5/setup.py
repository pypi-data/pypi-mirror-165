import os
import sys
import re
import setuptools
import numpy as np

from distutils.extension import Extension
from Cython.Build import cythonize


def find_version(filename):
    script_path = os.path.dirname(os.path.realpath(__file__))
    version_file = open(os.path.join(script_path, filename)).read()
    match = re.search(r'^__version__ = "(\d+\.\d+\.\d+)"', version_file, re.M)
    if match is not None:
        return match.group(1)
    raise RuntimeError("Unable to find version string.")


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EXtra-redu",
    version=find_version("src/extra_redu/__init__.py"),
    author="European XFEL GmbH",
    author_email="da-support@xfel.eu",
    maintainer="Egor Sobolev",
    url="https://git.xfel.eu/dataAnalysis/data-reduction",
    description="Tools for XFEL data quality estimation and data reduction",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="BSD-3-Clause",
    packages=setuptools.find_packages('src'),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        'extra_redu.lossy': ['*.h', '*.pyx', '*.pxd'],
    },
    ext_modules=cythonize(
        [
            Extension(
                "extra_redu.lossy.rounding",
                [
                    "src/extra_redu/lossy/rounding.pyx",
                    "src/extra_redu/lossy/rounding_impl.c"
                ],
                include_dirs=[np.get_include()],
            )
        ],
        compiler_directives={'language_level' : "3"},
    ),
    setup_requires=[
        'numpy',
        'cython',
    ],
    install_requires=[
        'numpy',
        'matplotlib',
        'euxfel-bunch-pattern>=0.6',
        'extra-data>=1.9.1',
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-cov',
            'mock',
          ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Utilities",
    ],
    python_requires='>=3.6',
)
