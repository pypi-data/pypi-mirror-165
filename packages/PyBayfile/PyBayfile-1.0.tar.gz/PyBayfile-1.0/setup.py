version = '1.0'

import setuptools

long_description = open('PyBayfile/README.md', 'r', encoding = 'utf-8').read()

setuptools.setup(
    name = 'PyBayfile',
    version = version,
    author = 'BlueRed',
    description = 'Module to integrate bayfiles and control them in your code',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/CSM-BlueRed/PyBayfile',
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    packages = setuptools.find_packages(),
    python_requires = '>=3.6',
    install_requires = ['aiohttp'],
    keywords = ['python', 'files', 'api', 'web', 'bayfile']
)