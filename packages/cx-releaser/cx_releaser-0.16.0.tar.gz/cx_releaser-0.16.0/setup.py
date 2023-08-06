import pathlib

# Always prefer setuptools over distutils
from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='cx_releaser',
    version='0.16.0',
    description='Python SDK to interact with docker registries',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/CiscoAandI/cx_releaser/',
    author='Aleksander Winski',
    author_email='awinski@cisco.com',
    classifiers=[
        'Topic :: Software Development :: Build Tools'
    ],
    keywords='cx releaser',
    entry_points={
        'console_scripts': [
            'cx_releaser=cx_releaser.scripts.command:main'
        ]
    },
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'boto3==1.20.47',
        'docker==5.0.3',
        'PyYaml>=5.4.0',
        'semantic-version==2.9.0',
        'docker-compose==1.29.2'
    ],
    project_urls={
        'Bug Reports': 'https://github.com/CiscoAandI/cx_releaser/issues',
        'Source': 'https://github.com/CiscoAandI/cx_releaser/',
    }
)
