from setuptools import setup

setup(
    name='apaato',
    version='1.0',

    packages=['apaato',],

    install_requires=[
        'selenium',
        'requests',
        'bs4',],

    entry_points={
        'console_scripts': [
            'apaato=apaato.main:main',
        ],
    },
)
