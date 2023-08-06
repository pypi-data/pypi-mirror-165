#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

requirements = [
    'ONE-api'
]

setup(
    name='pybpod-gui-plugin-alyx',
    version="1.1.3b1",
    description="""PyBpod Alyx API connection module""",
    author=['Sergio Copeto', 'Luís Teixeira'],
    author_email='sergio.copeto@research.fchampalimaud.org, ricardo.ribeiro@research.fchampalimaud.org, micboucinha@gmail.com',
    license='MIT',
    url='https://github.com/pybpod/pybpod-gui-plugin-alyx',

    include_package_data=True,
    packages=find_packages(),

    package_data={'pybpod_alyx_module': ['resources/*.*', ]},

    install_requires=requirements,
)
