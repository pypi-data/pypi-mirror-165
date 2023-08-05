from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name="webdriver-helper",
    version="1.0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data={
        "": [
            "upload_by_drop.js",
        ],
    },
    url="https://github.com/dongfangtianyu/webdriver-helper",
    author="dongfangtianyu",
    python_requires=">=3.9",
    description="自动下载浏览器驱动，使selenium 4.0开箱即用",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    install_requires=[
        "webdriver-manager==3.7.1",
        "selenium>=4.0.0",
    ],
)
