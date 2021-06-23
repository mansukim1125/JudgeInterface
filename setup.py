from setuptools import setup, find_packages
from os import path

this_dir = path.abspath(path.dirname(__name__))
with open(path.join(this_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='JudgeInterface',
    version='1.0.6',
    description='A DB Interface for Judge',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='mansu kim',
    author_email='mansukim1125@gmail.com',
    url='https://github.com/mansukim1125/JudgeInterface',
    license='MIT',
    python_requires='>=3',
    packages=['JudgeInterface', 'JudgeInterface/lib']
)
