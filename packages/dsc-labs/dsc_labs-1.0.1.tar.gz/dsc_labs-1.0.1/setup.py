#!/usr/bin/env python3
from setuptools import setup, find_packages
from dsc_labs.version import __prog__, __version__

setup(
    name=__prog__,
    version=__version__,
    description='Common libraries for DSC projects/services',
    author='Danh Nguyen.T',
    author_email='ntdanh1@tma.com.vn',
    url='https://gitlab.tma.com.vn/data-science-group/dsc-labs/-/tree/main/dsc_packages/common/python',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    keywords=['pip', 'dsc_labs', 'common'],
    install_requires=[
        'boto3>=1.17.49',
        'botocore>=1.20.49',
        'PyYAML>=5.1.2',
        'bugsnag>=3.6.0',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            '{0}-config=dsc_labs.cli.config:main'.format(__prog__)
        ]
    }
)
