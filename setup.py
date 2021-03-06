import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="catwalk",
    version="0.0.1",
    author="Simey de Klerk",
    author_email="simeydeklerk@gmail.com",
    description="A framework for Actuarial modelling.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/simeydk/catwalk",
    project_urls={
        "Bug Tracker": "https://github.com/simeydk/catwalk/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"catwalk": "catwalk"},
    packages=["catwalk"],
    python_requires=">=3.6",
    install_requires=["pandas", "numpy"],
    tests_require=["pytest"],
    include_package_data=True,
    package_data={"": ["tables/*.csv"]},
)
