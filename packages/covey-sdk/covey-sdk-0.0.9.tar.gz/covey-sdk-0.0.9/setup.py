import os
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    README = fh.read()

with open(os.path.join("requirements", "requirements.txt")) as reqs:
    REQUIREMENTS = reqs.readlines()

with open(os.path.join("requirements", "requirements_test.txt")) as reqs:
    REQUIREMENTS_TEST = reqs.readlines()

setup(
    name='covey-sdk',
    version='0.0.9',
    description='Covey Trading Tools',
    long_description= README,
    long_description_content_type='text/markdown',
    license='MIT',
    author="Vadim Serebrinskiy",
    author_email="vs@covey.io",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data = True,
    url='https://github.com/covey-io/ethereum-contract-interaction',
    keywords='covey',
    install_requires=REQUIREMENTS,
    tests_require=REQUIREMENTS_TEST,

)