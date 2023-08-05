from setuptools import setup, find_packages
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="TSDAL",
    version="0.0.2",
    author="runepic",
    author_email="759515344@qq.com",
    description="时空数据抽象库（TSDAL，Temporal and Spatial Data Abstraction Library)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # 项目主页
    # url="",

    # 你要安装的包，通过 setuptools.find_packages 找到当前目录下有哪些包
    package_dir={"": "src"},
    packages=find_packages(where="src"),

    python_requires=">=3.9",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]

)