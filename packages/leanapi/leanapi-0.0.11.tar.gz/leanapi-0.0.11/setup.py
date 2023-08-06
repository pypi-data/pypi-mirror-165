import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "leanapi",
    version = "0.0.11",
    author = "developerkitchen python team",
    author_email = "topluluk@developerkitchen.dev",
    description = ("Lean Api is a class layer for FastApi"),
    license = "MIT",
    keywords = "api, leanapi, fastapi",
    url = "http://github.com/developerkitchentr/leanapi",
    packages=['leanapi'],
    long_description_content_type = "text/markdown",
    long_description= read('README.md'),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        'fastapi>=0.63.0',
        'uvicorn>=0.13.3'
        'python-dotenv',
        'pydantic>=1.7.2'
    ]
)
