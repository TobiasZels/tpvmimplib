from setuptools import find_packages, setup

setup(
    name="tpvmimplib",
    packages=find_packages(),
    version='0.0.1',
    description='Library for the implementation of TPVM support for Python Programs.',
    author='Tobias Zels',
    install_requires=['socketio','uuid'],
    setup_requires=[],
    tests_requires=[],
    )