import os

from setuptools import setup

CURPATH = os.path.dirname(os.path.realpath(__file__))

PACKAGE_NAME = "hdlproxy"
SHORT_DESCRIPTION = "Proxy for PID handler"

VERSION = '0.1'

PACKAGES = ['hdlproxy']

# Package meta
CLASSIFIERS = []


requirements_file = os.path.join(CURPATH, "requirements.txt")
with open(requirements_file) as f:
    INSTALL_REQUIRES = [
        x.strip('\n')
        for x in f.readlines()
        if x and x[0] != '#'
    ]

EXTRAS_REQUIRES = {
}

TESTS_REQUIRES = [
]


setup(
    name=PACKAGE_NAME,
    version=VERSION,
    license='Affero GPL v3',
    author='Stavros Sachtouris @ GRNET S.A.',
    author_email='saxtouri@grnet.gr',
    description=SHORT_DESCRIPTION,
    classifiers=CLASSIFIERS,
    packages=PACKAGES,
    package_dir={'': '.'},
    # scripts=['manage.py'],
    zip_safe=False,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRES,
    tests_require=TESTS_REQUIRES,
    entry_points={},
)
