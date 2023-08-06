from setuptools import setup, find_packages

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
    name = "sbatcher",
    author = "Robert C. Gale",
    version="0.0.0a3",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={
        '': [
            'bin/*',
            '*.json',
        ]
    },
    scripts=['sbatcher/bin/sbatcher-array-job'],
)