from setuptools import setup, find_packages
import os
import codecs

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = "This package provide some python helper functions that are useful in machine learning."
# setting up
setup(
    name="helperfns",
    version=VERSION,
    author="Crispen Gari",
    author_email="<crispengari@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        "prettytable", "nltk", "sklearn", "matplotlib", "numpy", "torch"
    ],
    keywords=['python', 'python3', 'helper-functions', "text cleaning", "visualization", "machine-learning"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: MacOS X",
        "Environment :: MacOS X :: Carbon",
         "Environment :: MacOS X :: Carbon",
        "Environment :: MacOS X :: Cocoa",
        "Environment :: Web Environment",
        "Environment :: Win32 (MS Windows)",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Other Audience",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Education",
        "Topic :: Education :: Testing",
        "Topic :: Internet",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)