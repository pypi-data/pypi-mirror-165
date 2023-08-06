from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mathco",
    version="0.0.3",
    author="Abel Roy",
    author_email="abelroi007@gmail.com",
    description="Companion for your Mathematical Operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AbelR007/Mathco",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ]
)
