import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="usual",
    version="0.2.1",
    author="Lior Israeli",
    author_email="israelilior@gmail.com",
    description="Save all your repeated imports and their configurations at one place",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lisrael1/usual",
    project_urls={
        "Bug Tracker": "https://github.com/lisrael1/usual/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={"": ["*.xlsx"]},
    install_requires=[[]],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src", exclude=['*_tests', '*_examples'], ),
    python_requires=">=3.6",
)

