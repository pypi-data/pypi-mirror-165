from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.2.0'
DESCRIPTION = 'Dynamic Search in Array Field in Django Admin'
LONG_DESCRIPTION = 'A package that allows Dynamic Search in Array Field in Django Admin'

with open("README.md") as f:
    readme = f.read()
    DESCRIPTION += readme

# Setting up
setup(
    name="django_search_arrayfield",
    version=VERSION,
    author="Arshan Ahmad , Shivaank Tripathi",
    author_email="<arshan@thetarzanway.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    url="https://github.com/The-Tarzan-Way/django_search_arrayfield",
    packages=["django_search_arrayfield"],
    include_package_data=True,
    

    install_requires=[],
    keywords=['python', 'django_better_admin', 'dynamic_search', 'dynamic-search', 'django-admin'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)