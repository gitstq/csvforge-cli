#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSVForge-CLI Setup Script
"""

from setuptools import setup, find_packages
import os

# Read README
readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
long_description = ''
if os.path.exists(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='csvforge-cli',
    version='1.0.0',
    description='📊 CSVForge-CLI - Lightweight Terminal CSV Data Processing Engine',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='CSVForge Team',
    author_email='csvforge@example.com',
    url='https://github.com/gitstq/csvforge-cli',
    py_modules=['csvforge'],
    entry_points={
        'console_scripts': [
            'csvforge=csvforge:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
        'Topic :: Utilities',
    ],
    keywords='csv cli data-processing terminal toolkit json markdown converter',
    python_requires='>=3.8',
    license='MIT',
    project_urls={
        'Bug Reports': 'https://github.com/gitstq/csvforge-cli/issues',
        'Source': 'https://github.com/gitstq/csvforge-cli',
    },
)
