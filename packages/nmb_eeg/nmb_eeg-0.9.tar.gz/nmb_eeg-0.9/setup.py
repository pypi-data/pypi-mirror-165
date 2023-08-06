#!/usr/bin/python3

from setuptools import setup

with open('README_pypi.rst') as f:
    long_description = f.read()

setup(
    name='nmb_eeg',
    version='0.9',
    description="Power spectra of pure EEG from two temporarily paralysed subjects from Whitham et al 2007",
    long_description=long_description,
    author='Bernd Porr',
    author_email='bernd.porr@glasgow.ac.uk',
    py_modules=['nmb_eeg'],
    install_requires=['numpy'],
    zip_safe=False,
    url='https://github.com/berndporr/nmb_eeg',
    license='GPL 3.0',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
)
