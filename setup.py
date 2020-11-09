#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [ "pytest", "jinja2" ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Enrico Kaack",
    author_email='e.kaack@live.de',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A platform for clean code analysis.",
    entry_points={
        'console_scripts': [
            'ccap=ccap.ccap:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='ccap',
    name='ccap',
    packages=find_packages(include=['ccap', 'ccap.*']),
    setup_requires=setup_requirements,
    url='https://github.com/enrico-kaack/ccap',
    version='0.1.0',
    zip_safe=False,
)
