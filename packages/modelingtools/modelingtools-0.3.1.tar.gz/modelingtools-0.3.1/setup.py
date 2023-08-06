"""
https://packaging.python.org/guides/distributing-packages-using-setuptools/#distributing-packages
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="modelingtools",
    version="0.3.1",
    author="Jeremy Miller",
    author_email="jeremymiller00@gmail.com",
    description="Tools to make modeling easier - Work in progress",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jeremymiller00/modelingtools",
    project_urls={
        "Bug Tracker": "https://github.com/jeremymiller00/modelingtools/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=find_packages(),
    install_requires=["scikit-learn", "numpy", "matplotlib", "statsmodels", "pandas"],
    python_requires=">=3.7",
)