import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rosahami_processor",
    version="1.0.5",
    author="Michal Smid",
    author_email="m.smid@hzdr.de",
    description="tool to process SAXS data measured by using the HAPG SAXS mirror",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.hzdr.de/smid55/rosahami_processor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
