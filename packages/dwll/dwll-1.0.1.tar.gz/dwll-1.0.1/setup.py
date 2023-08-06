from setuptools import setup

import dwll

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='dwll',
    version=dwll.__version__,
    description=dwll.__doc__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=dwll.__keywords__,
    author=dwll.__author__,
    author_email=dwll.__email__,
    url=dwll.__url__,
    license=dwll.__license__,
    python_requires='>=3.5',
)