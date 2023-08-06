from setuptools import setup

setup(
    name='fileprotectorlib',
    version='0.0.1',
    packages=['fileprotectorlib'],
    install_requires=[
        'requests',
        'importlib; python_version == "3.8"',
    ],
)