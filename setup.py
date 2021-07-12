#!/usr/bin/env python3
from setuptools import setup

try:
    long_description = open('README.md', 'r').read()
except:
    long_description = ''

setup(
    name='poeditor-sync',
    version='0.3.1',
    packages=['poeditor_sync'],
    py_modules=['cmd'],
    entry_points={
        'console_scripts': ['poeditor = poeditor_sync.cmd:poeditor'],
    },
    url='https://github.com/mick88/poeditor-sync',
    license='MIT',
    author='Michal Dabski',
    author_email='contact@michaldabski.com',
    install_requires=[
        'click>=8',
        'poeditor',
        'pyyaml',
    ],
    description='Command line client for POEditor service',
    long_description_content_type='text/markdown',
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Utilities',
    ],
    project_urls={
        'Source': 'https://github.com/mick88/poeditor-sync',
        'Tracker': 'https://github.com/mick88/poeditor-sync/issues',
        'Changelog': 'https://github.com/mick88/poeditor-sync/blob/master/HISTORY.txt',
        'Example configuration': 'https://github.com/mick88/poeditor-sync/blob/master/example/poeditor.yml',
        'POEditor': 'https://poeditor.com/',
    },
)
