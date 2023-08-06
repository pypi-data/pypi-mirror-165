import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = "0.1.0"

setuptools.setup(
    name="pytest-fbu",
    version=version,
    author="vic",
    author_email="",
    description="pytest autoline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=["pytest_fbu"],
    include_package_data=True,
    install_requires=[
        "pytest",
    ],
    entry_points={"pytest11": ["pytest-fbu = pytest_fbu.core"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Framework :: Pytest",
    ],
    python_requires=">=3.7",
    setup_requires=["setuptools_scm"],
)
