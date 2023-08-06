import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as r:
    lines = [line.strip() for line in r.readlines()]
    running_idx = lines.index("# running")
    requirements = lines[running_idx + 1 :]
    print(requirements)


setuptools.setup(
    name="nqnq",
    version="0.1.8",
    author="nanangqq",
    author_email="gingggg@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    include_package_data=True,
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=requirements,
)
