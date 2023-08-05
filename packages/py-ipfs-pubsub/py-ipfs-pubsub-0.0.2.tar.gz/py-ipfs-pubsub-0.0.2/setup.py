import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-ipfs-pubsub",
    version="0.0.2",
    author="@ZachisGit",
    description="Pubsub client for python, since ipfshttpclient pubsub isn't compatibe with the newer versions of ipfs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["pubsub"],
    package_dir={'':'./'},
    install_requires=["requests>=2.23.0","py-multibase>=1.0.3"]
)