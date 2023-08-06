from setuptools import setup

setup(
    name='xkcd-comicdb',
    version='2022.08.31',
    description='SQLite3 database of every xkcd comic, scraped from the xkcd JSON API.',
    author='Noah Tanner',
    author_email='noahtnr@gmail.com',
    python_requires='>=3.7',
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: Free for non-commercial use",
        "Operating System :: OS Independent",
        "Topic :: Database",
    ],
    include_package_data=True,
)
