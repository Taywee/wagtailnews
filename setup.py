#!/usr/bin/env python
"""
Install wagtailnews using setuptools
"""
from setuptools import setup

with open('wagtailnews/version.py', 'r') as f:
    version = None
    exec(f.read())

with open('README.rst', 'r') as f:
    readme = f.read()

# Documentation dependencies
documentation_extras = [
    'Sphinx>=1.4.6',
    'sphinx-autobuild>=0.5.2',
    'sphinx_rtd_theme>=0.1.8',
    'sphinxcontrib-spelling==2.1.1',
    'pyenchant==1.6.6',
]

setup(
    name='wagtailnews-collection',
    version=version,
    description='News / blog plugin for the Wagtail CMS, but with news items belonging to collections, enforcing permissions',
    long_description=readme,
    author='Taylor C. Richberger',
    author_email='tcr@absolute-performance.com',
    url='https://github.com/taywee/wagtailnews-collection/',

    install_requires=[
        'wagtail>=1.5',
    ],
    extras_require={
        'docs': documentation_extras
    },
    zip_safe=False,
    license='BSD License',
    packages=[
        'wagtailnews',
        'wagtailnews.templatetags',
        'wagtailnews.views',
        ],
    include_package_data=True,
    package_data={
        'wagtailnews': [
            'templates/**/*.html',
            'templates/**/*.js',
            'static/**/*.js',
            'static/**/*.html',
            ]
        },
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
    ],
)
