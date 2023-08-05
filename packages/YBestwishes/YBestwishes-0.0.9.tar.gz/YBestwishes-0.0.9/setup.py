import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="YBestwishes",
    version="0.0.9",
    author="yone",
    author_email="1242925780@qq.com",
    description="A small fun package",
    url="https://github.com/yonesun/python-class",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["YBestwishes"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

)