from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = 'Find differences between two json files'
LONG_DESCRIPTION = 'A package that compares two input json files and returns the differences.'

# Setting up
setup(
    name="diff_finder",
    version=VERSION,
    author="Devidutta Sutar",
    author_email="<dev20sap@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    #install_requires=['json'],
    keywords=['python', 'json', 'compare'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)