from setuptools import find_packages, setup

setup(
    name="Winstree",
    version="0.0.1.alpha2",
    author="XiangQinxi",
    author_email="XiangQinxi@outlook.com",
    description="Windows环境.NET快速开发工具包",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    install_requires=[
        "pythonnet>=3.0.0a1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'gui_scripts': [
            'winstreer = Winstreer:empty_demo',
        ]
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"Winsdoc": ["*.txt", "*.html"]}
)
