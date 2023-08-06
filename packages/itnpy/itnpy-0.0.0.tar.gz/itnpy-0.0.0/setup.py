from setuptools import setup, find_packages

##########################################################################################################
name = "itnpy"
version = "0.0.0"
author = "Brandhsu"
author_email = "brandondhsu@gmail.com"
license = "MIT"
url = "https://github.com/Brandhsu/itnpy"
description = "A simple, deterministic, and extensible approach to inverse text normalization for numbers"
##########################################################################################################

with open("README.md", "r") as f:
    long_description = f.read()

packages = find_packages("src")

install_requires = [
    lib.strip()
    for lib in open("/Users/owner/Downloads/itnpy/requirements.txt").readlines()
]

setup(
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    license=license,
    url=url,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    package_dir={"": "src"},
    packages=packages,
    install_requires=install_requires,
    keywords=[
        "inverse text normalization",
        "natural language processing",
        "speech recognition",
        "itn",
        "nlp",
        "asr",
    ],
)
