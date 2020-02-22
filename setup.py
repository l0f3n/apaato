from setuptools import setup

setup(
    name='apaato',
    version='0.1.0',
    description='Calculates the probability of getting an accommodation at studentbostader.se.',
    url='https://github.com/l0f3n/apaato',
    author='Victor Löfgren',
    author_email='victor.l0fgr3n@gmail.com',
    packages=['apaato',],
    install_requires=[
        'requests',
        ],
    entry_points={
        'console_scripts': [
            'apaato=apaato.cli:main',
        ],
    },
    license='MIT',
)
