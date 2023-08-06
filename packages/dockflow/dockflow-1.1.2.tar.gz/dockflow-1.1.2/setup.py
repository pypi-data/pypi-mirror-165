import setuptools
import os

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    version = os.environ['CI_JOB_ID']

with open('README.md', 'r') as fh:
    long_description = fh.read()

EXCLUDE_FROM_PACKAGE = ['docs', 'tests*']

setuptools.setup(
    name="dockflow",
    version=version.strip('v'),
    license="Spatialedge Community License",
    author="Pieter van der Westhuizen",
    author_email="pieter@spatialedge.co.za",
    description="Easily deploy Airflow for local development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/spatialedge/public/dockflow",
    packages=setuptools.find_packages(exclude=EXCLUDE_FROM_PACKAGE),
    install_requires=[
        'click==7.1.2',
        'docker==4.2.2',
    ],
    entry_points='''
        [console_scripts]
        dockflow=dockflow.cli:main
    ''',
    setup_requires=['wheel'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True
)
