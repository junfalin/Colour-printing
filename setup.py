import setuptools

try:
    import pypandoc

    long_description = pypandoc.convert_file('README.md', 'rst')
except Exception:
    long_description = ""

setuptools.setup(
    name="colour-printing",
    version="0.3.14",
    author="faithforus",
    author_email="ljunf817@163.com",
    description="colour-printing",
    long_description=long_description,
    keywords="python package print",
    url="https://github.com/Faithforus/Colour-printing",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['cprint = colour_printing.cmdline:execute']
    },
)
