import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yb-wishes",
    version="0.0.8",
    author="yone",
    author_email="1242925780@qq.com",
    description="A small fun package",
    url="https://github.com/yonesun/python-class",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["yb-wishes"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

)