import logging
import os

from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def get_version():
    try:
        with open('PKG-INFO', 'r') as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith('Version:'):
                return line.split(':')[1].strip()
    except Exception:
        logging.info('Did not find PKG-INFO, getting build version from env variable')
        pass

    build_major = 0
    build_minor = os.getenv('GITHUB_RUN_NUMBER')
    if build_minor is None:
        raise Exception('GITHUB_RUN_NUMBER is not set')
    return f"{build_major}.5.{build_minor}"


version = get_version()

logging.info(f"Package version is '{version}'")

setup(
    name='django-simple-worker',
    version=version,
    description='Django Simple Worker',
    url='https://www.idea-loop.com/',
    author='idealoop',
    author_email='noreply@idea-loop.com',
    license='MIT',
    packages=find_packages(exclude=["tests.*", "tests", "test*"]),
    long_description=README,
    long_description_content_type='text/markdown',
    package_data={'': ['*.html']},
    include_package_data=True,
    install_requires=[
        'django',
        'apscheduler',
        'sentry-sdk',
    ],
    zip_safe=False
)
