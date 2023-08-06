from setuptools import setup

setup(
    name='capisce',
    version='0.0.2',
    install_requires=[
        'requests',
        'Flask',
        'ratelimit',
        'flask_cors'
    ],
    scripts=['src/capisce/capisce']
)
