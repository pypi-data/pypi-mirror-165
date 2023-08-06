from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


def get_version():
    version = {}
    with open("ensure_texlive/version.py") as f:
        exec(f.read(), version)
    return version["__version__"]


long_description = """**ensure_texlive** is a utility that installs
a small latex distribution (essentially a TinyTeX) in user mode on a user's machine.

Project home on gitlab: https://gitlab.com/peczony/ensure_texlive
"""


setup(
    name="ensure_texlive",
    version=get_version(),
    author="Alexander Pecheny",
    author_email="ap@pecheny.me",
    description="A small TeXLive distibution installer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/peczony/ensure_texlive",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["ensure_texlive"],
    install_requires=["requests"],
)
