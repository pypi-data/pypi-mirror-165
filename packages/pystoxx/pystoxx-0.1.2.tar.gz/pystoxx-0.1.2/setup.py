import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
        name="pystoxx",
        version="0.1.2",
        author="Saleh Alkhalifa",
        author_email="alkhalifas@recursiv.tech",
        description="Search and retrieve current data and historical information for publicly traded companies",
        url="https://github.com/recursivllc/pystoxx",
        keywords=['stock', 'prices', 'sentiment', 'historical', 'news', 'dataset', 'api'],
        install_requires=['requests'],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            ],
        packages=setuptools.find_packages(),
        python_requires='>3.6',
        long_description=long_description,
        long_description_content_type='text/markdown')
