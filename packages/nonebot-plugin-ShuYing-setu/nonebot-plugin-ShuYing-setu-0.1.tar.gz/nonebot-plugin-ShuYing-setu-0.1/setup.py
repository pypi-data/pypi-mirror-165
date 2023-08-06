import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nonebot-plugin-ShuYing-setu",
    version="0.1",
    author="SakuraPuare",
    author_email="java20131114@gmail.com",
    description="A setu plugin for NoneBot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SakuraPuare/nonebot-plugin-ShuYing-setu",
    packages=setuptools.find_packages(),
    install_requires=['httpx'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
