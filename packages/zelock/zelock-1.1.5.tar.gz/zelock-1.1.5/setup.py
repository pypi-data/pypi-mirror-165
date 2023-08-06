from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()
# use pypi account
setup(
    name="zelock",
    version='1.1.5',
    author="zenalyse",
    author_email="<thanat.th@zenalyse.co.th>",
    description='Package zelock',
    long_description_content_type="text/markdown",
    long_description='',
    packages=find_packages(),
    install_requires=[''],
    keywords=['zenalyse'],
    classifiers=["Programming Language :: Python :: 3"]
)
