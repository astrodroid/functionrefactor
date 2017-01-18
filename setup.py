import sys
sys.dont_write_bytecode = True

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

with open('README.rst') as file_readme:
    readme = file_readme.read()

setup(
    name='functionrefactor',
    version='0.0.2',
    description='Tidies up C++ headers. Moving C++ function implementations to the source file.',
    long_description=long_description,
    author='Andreas Angelopoulos',
    author_email='andreas.angelopoulos@gmail.com',
    license='MIT',
    url='',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='C++ cpp',
    packages=find_packages(),
    entry_points={
        'console_scripts':
        ['functionrefactor = functionrefactor.commands:execute'],
    },)
