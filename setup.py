"""
The Personas project
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import pip
from pip.req import parse_requirements


here = path.abspath(path.dirname(__file__))

install_reqs = parse_requirements('requirements.txt', session=pip.download.PipSession())
reqs = [str(ir.req) for ir in install_reqs]
setup(
    name='splineworks',
    version='0.1.0',
    description='Sand spline art',
    url='https://github.com/caged/splineworks',
    author='Justin Palmer',
    author_email='justin@labratrevenge.com',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # Pick your license as you wish (should match "license" above)
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License'
    ],

    # What does your project relate to?
    keywords='splines art datavisualization visualization',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['splineworks'],
    scripts=["scripts/splineworks"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=reqs,

    # dependency_links=[
    #     ''
    # ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'test': ['pytest==3.1.2'],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    # package_data={
    #     'sample': ['package_data.dat'],
    # },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={
    #     'console_scripts': [
    #         'nba-stats=json2csv',
    #     ],
    # },
)
