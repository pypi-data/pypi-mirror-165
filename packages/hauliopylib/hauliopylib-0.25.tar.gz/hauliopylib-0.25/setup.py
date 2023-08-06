import setuptools
import hauliopylib.version

print("Building version: {}".format(hauliopylib.version.__version__))

version = {}
with open("hauliopylib/version.py") as fp:
    exec(fp.read(), version)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hauliopylib",
    version=version['__version__'],
    author="Haulio Pte Ltd",
    author_email="data@haulio.io",
    description="This is a company library.",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://hauliov1@dev.azure.com/hauliov1/hauliopylib/_git/hauliopylib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)