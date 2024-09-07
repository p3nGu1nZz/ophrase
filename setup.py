# setup.py

from setuptools import setup, find_packages

setup(
    name='ophrase',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'tenacity',
        'rich',
        'ollama',
        'pydantic',
        'jinja2',
        'loguru',
    ],
    entry_points={
        'console_scripts': [
            'ophrase=ophrase.ophrase_main:main',
        ],
    },
)
