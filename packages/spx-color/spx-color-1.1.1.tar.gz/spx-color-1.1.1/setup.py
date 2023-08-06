import setuptools
from setuptools import setup
with open("README.md", "r", encoding="utf-8") as readme:
    read = readme.read()
setuptools.setup(
    name="spx-color",
    version='1.1.1',
    author="Spyrx",
    description="A Project can help you To Use The Color in Python",
    long_descripton= read,
    packges=["spx-color"],
    long_descripton_content_type="text/markdown",
    url= "https://github.com/SpYRx0/spx-color",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6"
)
