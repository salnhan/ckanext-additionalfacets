# -*- coding: utf-8 -*-

import sys, os

from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding
from os import path

version = '0.0.3-dev'

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='''ckanext-additionalfacets''',

    version=version,

    description="Easy to add custom facets to CKAN search, organizations and groups pages",

    long_description= long_description,

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        # 3 - Alpha
        # 4 - Beta
        # 5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],

    # What does your project relate to?
    keywords='''CKAN facets''',

    # Author details
    author='Minh Thien Nhan',
    author_email='timit06@yahoo.com',

    # Project's main homepage
    url='https://github.com/salnhan/ckanext-additionalfacets.git',

    # License of project
    license='GNU',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),

    namespace_packages=['ckanext'],

    include_package_data=True,

    zip_safe=False,

    install_requires=[],

    entry_points='''
        [ckan.plugins]
            additional_facets=ckanext.additionalfacets.plugins:AdditionalFacetsPlugin

        [paste.paster_command]
            additional_facets=ckanext.additionalfacets.commands:AdditionalFacetsCommand
    ''',
)