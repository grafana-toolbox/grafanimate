# -*- coding: utf-8 -*-
import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.rst")).read()

requires = [
    # Foundation
    "munch>=2.3,<3",
    "docopt>=0.6,<1",
    "tqdm>=4,<5",
    "unidecode>=1,<2",
    "furl>=2,<3",
    "dataclass-property>=1,<2",
    # Grafana control and animation
    "where>=1,<2",
    "marionette_driver>=3,<4",
    "python-dateutil>=2.7,<3",
    "datetime-interval==0.2",
    #'Pillow==5.2.0',
]

extras = {
    "test": [
        "pytest>=6,<7",
    ],
}

setup(
    name="grafanimate",
    version="0.5.5",
    description="Animate timeseries data with Grafana",
    long_description=README,
    license="AGPL 3, EUPL 1.2",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Telecommunications Industry",
        "Topic :: Communications",
        "Topic :: Database",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Archiving",
        "Topic :: System :: Networking :: Monitoring",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
    author="Andreas Motl",
    author_email="andreas.motl@panodata.org",
    url="https://github.com/panodata/grafanimate",
    keywords="grafana animate animation automation time gif video",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "grafanimate": [
            "*.js",
        ],
    },
    zip_safe=False,
    test_suite="grafanimate.test",
    install_requires=requires,
    extras_require=extras,
    tests_require=extras["test"],
    dependency_links=[],
    entry_points={
        "console_scripts": [
            "grafanimate = grafanimate.commands:run",
        ],
    },
)
