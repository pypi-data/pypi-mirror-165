from setuptools import find_packages, setup


CLASSIFIERS = [
    'Intended Audience :: Developers',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.10',
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mpylogs',
    packages=find_packages(include=['mpylogs']),
    version='0.0.1',
    description='Python library for logging with colors and http status code.',
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/jeniferss/_logging',
    install_requires=[],
    classifiers=CLASSIFIERS,
    keywords='logs logging logger',
    python_requires = '>=3.10',
)
