from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.9'
DESCRIPTION = "A simplified webscraper that's based on Selenium."
LONG_DESCRIPTION = "A simplified webscraper that's based on Selenium."

# Setting up
setup(
    name="carpetsWebScraper",
    version=VERSION,
    author="thecarpetjasp",
    author_email="thecarpetjasp@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['selenium','pandas','bs4','requests'],
    keywords=['python', 'selenium', 'webscraper'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)