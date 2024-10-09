from setuptools import setup, find_packages

setup(
    name="zignpay",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    author="Kevelino",
    author_email="kevinnengou02@gmail.com",
    description="A package to manage mobile payments using the MTN MoMo and Orange Money APIs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kevelino/zignpay",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)