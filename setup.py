import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyufw",
    packages=['pyufw'],
    version="0.0.3",
    author="Callum Ray",
    author_email="callumray@hotmail.co.uk",
    description="A Python wrapper for UFW",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/5tingray/pyufw",
    classifiers=[
        "Programming Language :: Python :: 3",
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
    ],
    python_requires='>=3',
)
