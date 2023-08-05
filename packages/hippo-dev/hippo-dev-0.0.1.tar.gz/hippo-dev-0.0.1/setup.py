import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="hippo-dev",
    version="0.0.1",
    author="Ben Pearce",
    author_email="benjamin.j.pearce@outlook.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://idea-org.github.io/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.8",
    install_requires=[],
)
