from setuptools import setup

setup(
    name='icenews',
    version='1.0',
    description='Simple NLP for Icelandic News',
    url='http://github.com/sverrirab/icenews',
    author='Sverrir A. Berg',
    author_email='sab@keilir.com',
    license='Apache',
    packages=[
        'icenews'
    ],
    zip_safe=False,
    install_requires=[
        'Flask-RESTful>=0.3.7',
        'reynir>=1.5.1',
    ]
)
