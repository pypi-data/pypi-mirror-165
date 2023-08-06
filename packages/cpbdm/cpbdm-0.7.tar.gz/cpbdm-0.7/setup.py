from setuptools import setup, find_packages
import setuptools

# To use a consistent encoding
from codecs import open
from os import path

setup(
    name='cpbdm',
    version='0.7',
    license='MIT',
    author="mahdi",
    author_email='sellingavl@gmail.com.com',
    packages=find_packages('cpbdm'),
    package_dir={'': 'cpbdm'},
    url='',
    keywords='example project',
    setup_requires = [
        'pytest-runner',
        'pypandoc>=1.4',
    ],
    install_requires = [
        'matplotlib>=2.0.0',  # This should be a dependency of `scikit-image`
        'numpy>=1.11.1',
        'scikit-image>=0.12.3',
        'scipy>=0.18.1',
    ],
    tests_require = ['pytest'],
    extras_require = {
        'dev': [
            'pandas>=0.19.2',
            'pytest>=3.0.0',
            'scikit-learn>=0.18.1',
            'tox>=2.9.1',
        ],
       },
)
