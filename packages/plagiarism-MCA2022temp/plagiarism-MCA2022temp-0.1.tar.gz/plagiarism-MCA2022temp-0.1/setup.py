import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="plagiarism-MCA2022temp",
    version="0.1",
    author="Piyush Devda",
    author_email="piyushdevda03@gmail.com",
    description="A Simple Plagiarism Checker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mnk-q/plagy",
    install_requires=['scikit-learn'],
    project_urls={
        "Bug Tracker": "https://github.com/mnk-q/plagy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)