import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="amnesiac_engine",
    version="0.1.4",
    author="BeckATI",
    author_email="hire.abeck@gmail.com",
    description="A WIP 2D game engine based on Pyglet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/beckadamtheinventor/amnesiac-engine",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)