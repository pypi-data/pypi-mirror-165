import os

from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), fname), "r") as fin:
        return fin.read()


setup(
    name = "aws-easy-use",
    version = "0.0.5",
    author = "Ted Chen",
    author_email = "imaging8896@gmail.com",
    description = "AWS boto3 wrapper. Make it easier and intuitive to use.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    license = "MIT",
    url = "https://github.com/imaging8896/aws-easy-use",
    project_urls={
        # 'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
        # 'Funding': 'https://donate.pypi.org',
        'Source': "https://github.com/imaging8896/aws-easy-use",
        # 'Tracker': 'https://github.com/pypa/sampleproject/issues',
    },
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3",
    install_requires=[
        "boto3>=1.24.28"
    ],
    # setup_requires=[
    #     "feedparser>=5.1.3",
    # ],
    # see http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3 :: Only",
    ],
)