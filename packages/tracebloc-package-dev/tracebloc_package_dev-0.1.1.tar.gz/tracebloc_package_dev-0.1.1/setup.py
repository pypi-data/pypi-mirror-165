import setuptools

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="tracebloc_package_dev",
    version="0.1.1",
    description="Package required to run Tracebloc jupyter notebook to create experiment",
    url="https://gitlab.com/tracebloc/tracebloc-py-package/-/tree/dev",
    license="MIT",
    python_requires=">=3",
    packages=["tracebloc_package"],
    author="Tracebloc",
    author_email="pallav@tracebloc.io",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["requests", "termcolor", "rich"],
    zip_safe=False,
)
