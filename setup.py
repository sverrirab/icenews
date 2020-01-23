from os import path
from setuptools import setup

README = "README.md"
VERSION_FILE = "version.txt"
REQUIREMENTS = "requirements.txt"
REQUIREMENTS_TEST = "requirements_test.txt"

here = path.abspath(path.dirname(__file__))
with open(path.join(here, VERSION_FILE), encoding="utf-8") as f:
    VERSION = f.read()
with open(path.join(here, README), encoding="utf-8") as f:
    long_description = f.read()


def get_requirements(filename):
    requires = []
    with open(path.join(here, filename)) as f:
        for line in f.readlines():
            req = line.split("#")[0].strip()
            if req:
                requires.append(req)
    return requires


setup(
    name="icenews",
    version=VERSION,
    description="Simple NLP for Icelandic News",
    url="https://github.com/sverrirab/icenews",
    author="Sverrir A. Berg",
    author_email="sab@keilir.com",
    license="Apache",
    keywords="nlp, icelandic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["icenews"],
    include_package_data=True,
    install_requires=get_requirements(REQUIREMENTS),
    test_requires=get_requirements(REQUIREMENTS_TEST),
    scripts=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={"console_scripts": ["icenews = icenews:main"]},
)
