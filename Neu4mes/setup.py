import setuptools

from neu4mes import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="neu4mes",
    version=__version__,
    author="Gastone Pietro Rosati Papini",
    author_email="tonegas@gmail.com",
    description="The final framework neural network for mechanics modeling and control",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tonegas/neu4mes",
    packages=setuptools.find_packages(),
    platforms='any',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>3.6'
)