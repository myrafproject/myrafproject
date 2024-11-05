from setuptools import setup, find_packages

setup(
    name='myraf',
    version='3.1',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    py_modules=['main'],
    entry_points={
        'console_scripts': [
            'myraf = myraf_gui:main',
            'im = commands:main',
        ],
    },
    install_requires=[
    ],
)
