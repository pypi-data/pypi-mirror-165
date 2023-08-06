"""
=========================
File: setup.py.py
Author: dancing
Time: 2022/8/28
E-mail: zhangqi_xxs@163.com
=========================
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zhaogang_collection",
    version="0.0.1",
    author="zuiqiu",
    author_email="zhangqi_xxs@163.com",
    description="decode unicode-eacape",
    long_description='no long_description',
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    # project_urls={
    # 	"Bug Tracker": "https://github.com/pypa/sampleproject/issues"
    # },
    classifiers=[
        "Framework :: Pytest",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Programming Language :: Python :: 3.7",
    ],
    license='proprietary',
    packages = setuptools.find_packages(),
    keywords=[
        'pytest', 'py.test', 'zhaogang_collection',
    ],
    # packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)