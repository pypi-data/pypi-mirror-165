import setuptools

setuptools.setup(
    name="Tklie",
    version="0.0.1.dev1",
    author="XiangQinxi",
    author_email="XiangQinxi@outlook.com",
    description="使用tkinter和tkdev4开发的功能库。",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://xiangqinxidevelopment.jetbrains.space/p/tkinterdev",
    python_requires=">=3.6",
    install_requires=[
        "Pillow",
        "colorama",
        "tkdev4",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
