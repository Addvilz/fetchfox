#!/usr/bin/env python

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='fetchfox',
    version='1.0.1',
    description='Fetchfox automates installation of Firefox on Linux systems',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Addvilz',
    author_email='mrtreinis@gmail.com',
    url='https://github.com/Addvilz/fetchfox',
    download_url='https://github.com/Addvilz/fetchfox',
    license='Apache 2.0',
    platforms='UNIX',
    packages=find_packages(),
    install_requires=[
        'wget>=3.1'
    ],
    entry_points={
        'console_scripts': [
            'fetchfox = fetchfox.main:main',
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3 :: Only'
    ],
)
