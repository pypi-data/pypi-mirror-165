import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scrapy-tor-proxy-rotator",
    version="0.0.2",
    author="Dragos Popa ",
    author_email="dragospopa420@gmail.com",
    description="Rotate TOR IPs with Scrapy (forked from scrapy-tor-proxy-rotation 0.0.1)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dragospopa420/scrapy-tor-proxy-rotation",
    packages=setuptools.find_packages(),
    install_requires=[
        'pysocks>=1.7.1',
        'requests>=2.23.0',
        'stem>=1.8.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    python_requires='>=3.6',
)
