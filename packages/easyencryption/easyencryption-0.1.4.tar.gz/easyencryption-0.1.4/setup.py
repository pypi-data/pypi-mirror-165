from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_desc = open("README.md", "r")
long_description = long_desc.read()
##with open('src/easyencryption/__init__.py', 'r') as f:
    ##version = [line.split('=')[1].strip(" '\"") for line in f.read().splitlines() if line.startswith('__version__')][0]
version = "0.1.4"

setup(
    name='easyencryption',
    version=version,
    description='A very easy way to encrypt data.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/BlazenBoi/easyencryption/issues',
    author='Blazen',
    author_email='contact@fireballbot.com',
    keywords='',
    packages=find_packages(include=['easyencryption']),
    python_requires='>=3.6',
    install_requires=[
    "setuptools>=42",
    "cryptography",
    "pycryptodomex",
    "pycryptodome",
    "wheel"
    ],
    project_urls={
        'Discord Server': 'https://discord.com/invite/mPU3HybBs9',
        'Bug Tracker': 'https://github.com/BlazenBoi/easyencryption/issues',
        'Source': 'https://github.com/BlazenBoi/easyencryption',
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
      ]
)
#© 2021 GitHub, Inc.