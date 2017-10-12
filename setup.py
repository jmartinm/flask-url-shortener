# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='url_shortener',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask==0.12.2',
        'Flask-Caching==1.3.3',
        'Flask-SQLAlchemy==2.3.2',
        'SQLAlchemy-Utils==0.32.18',
        'psycopg2==2.7.3.1',
        'redis==2.10.6',
        'gunicorn==19.7.1'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
