from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.4'
DESCRIPTION = "A password cracking tool."
LONG_DESCRIPTION = "A tool that will allow you to crack passwords. This library can generate password dictionaries for a brute-force attack and can also automatically crack any hash for you."

# Setting up
setup(
    name="pwdcrk",
    version=VERSION,
    author="thecarpetjasp",
    author_email="thecarpetjasp@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['hashlib'],
    keywords=['python', 'password', 'password cracker', 'brute-force', 'dictionary'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)