from setuptools import setup, find_packages

setup(
    name='capisce',
    version='0.0.7',
    packages=find_packages(),
    install_requires=[
        'requests',
        'Flask',
        'ratelimit',
        'flask_cors'
    ],
    entry_points={
        'console_scripts': [
            'capisce = main:run',
        ],
    },
)
