#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name="spol",
    version="0.0.1",
    keywords=["pakistan", "sindh", "police", "complaint", "query", "search", "units"],

    description="Pakistan Sindh Police",
    long_description=open('README.md').read(),

    project_urls={
        'Homepage': 'https://www.techtum.dev/work-spcs-220121.html#work-spol-220121',
        'Source': 'https://github.com/siphr/spol',
        'Tracker': 'https://github.com/siphr/spol/issues',
    },

    author="siphr",
    author_email="pypi@techtum.dev",

    packages=['spol'],
    platforms="any",
)
