from setuptools import setup, find_packages

setup(
    name='myraf',
    version='3.0',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    py_modules=['main'],
    entry_points={
        'console_scripts': [
            'myraf = main:main',
        ],
    },
    install_requires=[
    ],
)

