
#!/usr/bin/env python3.8
from setuptools import setup, find_packages

description = "A CLI tool for bumping semantic versions"
with open("README.md", "r") as f:
  long_description = f.read()

setup(
    name="sem-bump",
    version="0.0.1",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mathew Moon",
    author_email="me@mathewmoon.net",
    # Choose your license
    python_requires=">=3.8",
    url="https://github.com/mathewmoon/sem-bump",
    license="Apache 2.0",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
    ],
    install_requires=["semantic-version"],
    entry_points = {
      "console_scripts": [
        "sem-bump = sem_bump:main"
      ]
    },
    packages=["sem_bump"]
)
