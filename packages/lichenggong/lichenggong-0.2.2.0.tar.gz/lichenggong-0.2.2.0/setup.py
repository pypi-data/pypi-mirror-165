import setuptools

with open("README.md","r",encoding="utf-8") as f:
    long_description=f.read()
setuptools.setup(
    name="lichenggong",
    version="0.2.2.0",
    author="2368916680",
    author_email="2368916680@qq.com",
    description="语言：简体中文 操作系统：windows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=None,
    include_package_data=True,
    package_data={
    'lichenggong':['ikun/*.*','废弃程序/*.py','zh_CN/*.*','en_US/*.*']
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    python_requires=">=3"
)
