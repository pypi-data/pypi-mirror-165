from setuptools import find_packages, setup

with open('README_PUB.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="ubicquia",
    package=find_packages(include=["ubicquia"]),
    # package=["ubicquia"],
    version="0.0.1",
    description="Ubicquia API Client Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://<site>.readthedocs.io/",
    license="GPLv3",
    author="CiberC Dev",
    install_requires=[
        'requests>=2.28',
        'requests-oauthlib',
        'python-decouple',
        'pydantic>=1.9'
    ],
)
