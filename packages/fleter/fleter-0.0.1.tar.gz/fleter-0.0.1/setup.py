from setuptools import find_packages, setup

setup(
    name="fleter",
    version="0.0.1",
    author="XiangQinxi",
    author_email="XiangQinxi@outlook.com",
    description="flet extension library",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    install_requires=[
        "flet",
    ],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'gui_scripts': [
            'fleter-demo = fleter_demo:run',
        ],
    },
)
