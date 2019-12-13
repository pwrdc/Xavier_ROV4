import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LogPy",
    version="0.0.1",
    author="Piotr Zielinski, Dominik Wasiolka",
    author_email="piotr_zielinski@g.pl",
    description="Versatile Python logger",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PiotrJZielinski/LogPy",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
