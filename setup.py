import setuptools
import codecs
import os


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


setuptools.setup(
    name="colour-printing",
    version="0.0.8",
    author="faithforus",
    author_email="ljunf817@163.com",
    description="colour-printing",
    long_description=read('README.rst'),
    keywords="python package print",
    url="https://github.com/Faithforus/Colour-printing",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
