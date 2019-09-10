import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


def get_version():
    with open("VERSION") as fi:
        return fi.read().strip()


setuptools.setup(
    name="recipe-transformer",
    version=get_version(),
    author="Thomas Corcoran",
    author_email="chasecorcoran@gmail.com",
    description="Automatic Recipe Generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tccorcoran/recipetransformer",
    packages=setuptools.find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
