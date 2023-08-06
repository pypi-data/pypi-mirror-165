# Copyright (C) 2022 Panther Labs Inc
#
# Panther Enterprise is licensed under the terms of a commercial license available from
# Panther Labs Inc ("Panther Commercial License") by contacting contact@runpanther.com.
# All use, distribution, and/or modification of this software, whether commercial or non-commercial,
# falls under the Panther Commercial License to the extent it is permitted.

# coding=utf-8
# *** WARNING: generated file
from setuptools import setup, find_packages


# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='panther_config',
    url="https://panther.com",
    author="Panther Labs Inc.",
    author_email="support@panther.io",
    version='0.0.13',
    packages=find_packages(),
    package_data={"panther_config": ["py.typed"]},
    python_requires=">=3.9",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='security detection',
    install_requires=[
        'panther_core>=0.3.0,<0.4.0',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Security',
        'Typing :: Typed',
        'Programming Language :: Python :: 3',
    ]
)
