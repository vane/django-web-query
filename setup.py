from setuptools import setup

import djangowebquery

setup(
    name="django-web-query",
    version=weborm.__version__,
    description="REST style querysets for django",
    long_description="Extends django querysets with ability to call directly from web browser",
    keywords="django, views, api explorer",
    author="Michal Szczepanski <michal@vane.pl>",
    author_email="michal@vane.pl",
    url="https://github.com/vane/django-web-query",
    license="BSD",
    packages=["djangowebquery"],
    zip_safe=False,
    install_requires=["dateutil"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
        "Development Status :: 1 - Alpha",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7"
    ],
)