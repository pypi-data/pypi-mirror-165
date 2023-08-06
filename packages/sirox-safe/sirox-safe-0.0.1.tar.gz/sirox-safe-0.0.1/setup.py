from setuptools import setup, find_namespace_packages

setup(
    name="sirox-safe",
    version="0.0.1",
    description="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["safe-eth-py==4.4.0", "requests"],
    packages=find_namespace_packages(include=["sirox.*"]),
)
