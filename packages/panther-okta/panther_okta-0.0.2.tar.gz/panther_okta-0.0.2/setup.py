from pathlib import Path
from setuptools import setup, find_packages

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
version = (this_directory / "VERSION").read_text()

setup(
    name='panther_okta',
    url="https://panther.com",
    author="Panther Labs Inc.",
    author_email="support@panther.io",
    version=version,
    packages=find_packages(),
    python_requires=">=3.9",
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='security detection',
    install_requires=[
        'panther_config>=0.0.13,<0.1.0',
        'panther_utils>=0.0.4,<0.1.0',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Security',
        'Typing :: Typed',
        'Programming Language :: Python :: 3',
    ]
)
