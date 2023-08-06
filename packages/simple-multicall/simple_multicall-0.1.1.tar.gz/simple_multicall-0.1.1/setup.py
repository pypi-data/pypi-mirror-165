from setuptools import setup, find_packages

VERSION = '0.1.1' 
DESCRIPTION = 'Simple Web3 multicall'
LONG_DESCRIPTION = 'Simple multicall implementation for use with Web3 library'

setup(
    name='simple_multicall',
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author='Igor Lapshin',
    author_email= 'igorlapshin@list.ru',
    packages=find_packages(),
    license='MIT',
    keywords=['multicall', 'web3'],
    requires=['Web3'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ]
)