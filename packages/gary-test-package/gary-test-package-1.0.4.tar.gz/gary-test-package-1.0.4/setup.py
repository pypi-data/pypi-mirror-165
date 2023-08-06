import os
from setuptools import setup, find_packages
from packaging.version import Version

# Try to read version string from env variable
# Default to 0.0.1`
version_string = os.environ.get("NEXT_TAG_VERSION", "0.0.1")
version = Version(version_string)

setup(
    name='gary-test-package',
    version=str(version),
    license='MIT',
    author="Gary Schaetz",
    author_email='gary@schaetzkc.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='',
    keywords='',
    install_requires=[],
)
