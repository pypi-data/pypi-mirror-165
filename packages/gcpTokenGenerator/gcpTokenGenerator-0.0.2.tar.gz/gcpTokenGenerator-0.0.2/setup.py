import os
from setuptools import find_packages, setup

##
# @file
# @brief This setup.py file is used for creating a Pkg from the ds-framework.
#        In order to be able to pip install ds-framework.

with open('requirements.txt') as f:
    required = f.read().splitlines()


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='gcpTokenGenerator',
    packages=find_packages(),
    py_modules=['gcpTokenGenerator'],
    version='0.0.2',
    description='google token generator',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    # url='http://pypi.python.org/pypi/PackageName/',
    author='oribrau@gmail.com',
    license='MIT',
    install_requires=required,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)

# Commands
# for test -  python setup.py pytest
# for build wheel -  python setup.py bdist_wheel
# for source dist -  python setup.py sdist
# for build -  python setup.py build
# for install -  python setup.py install
# for uninstall - python -m pip uninstall gcpTokenGenerator
# for install - python -m pip install dist/gcpTokenGenerator-0.0.1-py3-none-any.whl
# for installing from the local work dir - pip install <path to local directory>

# Deploy to PyPI
# delete dist and build folders
# python setup.py clean --all
# python setup.py bdist_wheel
# python setup.py sdist
# python setup.py build
# twine upload dist/*
'''
    use
    1. python setup.py install
    2. dsf-cli g model new_model_name
    3. twine check dist/*
    4. twine upload --repository-url https://pypi.org/legacy/ dist/*
    4. twine upload dist/*
    
    pip install gcpTokenGenerator --index-url https://pypi.org/simple
    
    how to use
    
    pip install gcpTokenGenerator
    
    dsf-cli generate project my-new-model
'''
