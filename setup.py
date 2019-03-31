from os import path
from setuptools import setup

VERSION = '1.0.3'
README = 'README.md'
REQUIREMENTS = 'requirements.txt'
PACKAGE_DATA = [README, 'LICENSE']

here = path.abspath(path.dirname(__file__))
with open(path.join(here, README), encoding='utf-8') as f:
    long_description = f.read()

requires = []
with open(path.join(here, REQUIREMENTS)) as f:
    for l in f.readlines():
        req = l.split('#')[0].strip()
        if req:
            requires.append(req)

setup(
    name='icenews',
    version=VERSION,
    description='Simple NLP for Icelandic News',
    url='https://github.com/sverrirab/icenews',
    author='Sverrir A. Berg',
    author_email='sab@keilir.com',
    license='Apache',
    keywords='nlp, icelandic',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=[
        'icenews'
    ],
    package_data={'': PACKAGE_DATA},
    include_package_data=True,
    install_requires=requires,
    scripts=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    entry_points={'console_scripts': [
        'icenews = icenews:main',
    ]},

)
