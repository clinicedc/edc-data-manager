# -*- coding: utf-8 -*-
import os
from setuptools import setup
from setuptools import find_packages
from os.path import join, abspath, normpath, dirname

with open(join(dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

with open(join(dirname(__file__), 'VERSION')) as f:
    VERSION = f.read()

tests_require = ['edc-test-utils', 'coverage']
with open(join(dirname(abspath(__file__)), 'requirements.txt')) as f:
    for line in f:
        tests_require.append(line.strip())

# allow setup.py to be run from any path
os.chdir(normpath(join(abspath(__file__), os.pardir)))

setup(
    name='edc-data-manager',
    version=VERSION,
    author=u'Erik van Widenfelt',
    author_email='ew2789@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/clinicedc/edc-data-manager',
    license='GPL license, see LICENSE',
    description='Data manager administrative models and classes',
    long_description=README,
    zip_safe=False,
    keywords='django base classes for identifiers',
    install_requires=[
        "django-audit-fields",
        "edc-action-item",
        "edc-appointment",
        "edc-auth",
        "edc-constants",
        "edc-form-validators",
        "edc-lab",
        "edc-list-data",
        "edc-metadata",
        "edc-model",
        "edc-model-admin",
        "edc-registration",
        "edc-sites",
        "edc-utils",
        "edc-visit-schedule",
        "celery",
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    python_requires=">=3.7",
    tests_require=tests_require,
    test_suite='runtests.main',
)
