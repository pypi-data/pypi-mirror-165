from setuptools import setup, find_packages

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="ofrak_type",
    version="0.0.1",
    description=("OFRAK: unpack, modify, and repack binaries."),
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Red Balloon Security",
    url="https://ofrak.com",
    packages=["ofrak_type"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Topic :: Security",
        "Topic :: Software Development :: Embedded Systems",
        "Typing :: Typed",
    ],
    python_requires=">=3.7",
)
