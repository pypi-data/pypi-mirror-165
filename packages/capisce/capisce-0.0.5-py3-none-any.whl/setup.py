from setuptools import setup, find_packages

setup(
    name='capisce',
    version='0.0.5',
    packages=find_packages(),
    install_requires=[
        'requests',
        'Flask',
        'ratelimit',
        'flask_cors'
    ],
    scripts=['capisce/capisce.py']
)
