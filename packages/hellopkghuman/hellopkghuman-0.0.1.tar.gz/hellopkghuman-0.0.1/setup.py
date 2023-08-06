from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = 'Testin PyPi'


# Setting up
setup(
    name="hellopkghuman",
    version=VERSION,
    author="Human",
    author_email="<human@freitagsrunde.org>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
