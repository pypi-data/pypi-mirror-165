from setuptools import setup, find_packages

# read in version string
VERSION_FILE = 'kernelquantifier/_version.py'
__version__ = None  # to avoid inspection warning and check if __version__ was loaded
exec(open(VERSION_FILE).read())

if __version__ is None:
    raise RuntimeError(
        "__version__ string not found in file %s" % VERSION_FILE)

# README
with open("README.md", "r") as fh:
    long_description = fh.read()

# requires
reqs = ['torch',
        'numpy',
        'matplotlib',
        'cvxopt',
        'tqdm',
        'pykeops'
        ]

# SETUP
setup(
    name='kernelquantifier',
    version=__version__,
    packages=find_packages(),
    description='Quantification using Kernel Embedding and Random Fourier Features. On GPU and CPU.',
    url='https://gitlab.com/bastiendussapapb/kernelquantifier',
    install_requires=reqs,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Development Status :: 4 - Beta",
        "Environment :: GPU :: NVIDIA CUDA",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    author='Bastien Dussap',
    author_email='bastien.dussap@inria.fr',
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
)