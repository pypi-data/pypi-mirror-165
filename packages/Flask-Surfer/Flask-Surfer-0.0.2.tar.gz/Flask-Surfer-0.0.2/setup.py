"""
Flask-Surfer
------------

Extension to add CSRF protection to flask applications.
"""

from setuptools import setup

setup(
    name="Flask-Surfer",
    version="0.0.2",
    license="MIT",
    author="John Kyle Alas-as",
    author_email="alasasjohnkyle@gmail.com",
    url="https://github.com/jkalasas/Flask-Surfer",
    download_url="https://github.com/jkalasas/Flask-Surfer/archive/refs/tags/0.0.2.tar.gz",
    long_description=__doc__,
    keywords=[
        "csrf",
        "flask",
        "protection",
        "security",
    ],
    packages=[
        "flask_surfer",
    ],
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requirements=[
        "flask",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
