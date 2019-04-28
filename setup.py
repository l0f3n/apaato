from setuptools import setup

setup(
    name='apaato',
    version='1.0',

    packages=['apaato',],

    install_requires=[
        'selenium',
        'requests',
        'lxml',
        'bs4',],

    entry_points={
        'console_scripts': [
            'apaato=apaato.command_line_interface:main',
        ],
    },
)
