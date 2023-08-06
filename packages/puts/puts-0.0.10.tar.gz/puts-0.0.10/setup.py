from setuptools import find_namespace_packages, setup

MAJOR = 0
MINOR = 0
MICRO = 10
VERSION = "%d.%d.%d" % (MAJOR, MINOR, MICRO)

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="puts",
    version=VERSION,
    author="Mark H. Huang",
    author_email="dev@markhh.com",
    description="Python Utility Tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MarkHershey/puts",
    license="MIT",
    packages=find_namespace_packages(include=["puts", "puts.*"]),
    install_requires=["colorlog>=4.1.0", "numpy"],
    extras_require={
        "dev": [
            "check-manifest",
            "pytest",
            "tox",
            "twine",
            "wheel",
        ]
    },
    keywords=[
        "utilities",
        "toolkit",
        "toolbox",
        "logger",
    ],
    # Classifiers ref: https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        # "Framework :: tox",
        "Framework :: Pytest",
    ],
    python_requires=">=3.6",
)
