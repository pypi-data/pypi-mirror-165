import setuptools

setuptools.setup(
    name="tkdev4",
    version="4.2.6",
    author="XiangQinxi",
    author_email="XiangQinxi@outlook.com",
    description="tkinterDev超级工具库，仅为Windows开发支持。",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://xiangqinxidevelopment.jetbrains.space/p/tkinterdev",
    python_requires=">=3.6",
    install_requires=[
        "tqdm",
        "colorama",
        "windnd", 
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
