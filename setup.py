import setuptools

setuptools.setup(
    name="jcon",
    version="0.1.0",
    author="MitawaUT",
    author_email="sota.misawa@akariinc.co.jp",
    description="easy way to deal with json file as configs in python.",
    long_description="This repository removes the boiler plate to use a json file as a config.",
    long_description_content_type="text/markdown",
    url="https://akariinc.co.jp/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
