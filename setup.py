from setuptools import setup, find_packages

DISTNAME = "snl-progress"
VERSION = "2.0.0"
PYTHON_REQUIRES = ">=3.11"
DESCRIPTION = "Used to evaluate the reliability of a power system and size energy storage systems required for maintaining a certain reliability level"
LONG_DESCRIPTION = open("README.md").read()
AUTHOR = "Sandia National Laboratories"
MAINTAINER_EMAIL = "abera@sandia.gov"
LICENSE = "BSD 3-clause"
URL = "https://github.com/sandialabs/snl-progress"


setup(
    name=DISTNAME,
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    python_requires=PYTHON_REQUIRES,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    maintainer_email=MAINTAINER_EMAIL,
    license=LICENSE,
    url=URL,
    install_requires=[
        "numpy>=1.21.0,<2.0.0",
        "pyomo==6.7.3",
        "pandas==2.2.2",
        "matplotlib==3.9.0",
        "openpyxl==3.1.4",
        "seaborn==0.13.2",
        "scikit-learn==1.5.0",
        "kneed==0.8.5",
        "requests==2.32.4",
        "pvlib==0.11.0",
        "NREL-rex==0.2.86",
        "PySide6==6.5.2",
        "PySide6-Addons==6.5.2",
        "PySide6-Essentials==6.5.2",
        "Markdown==3.7",
        "plotly==5.24.1",
        "kaleido==0.2.1",
        "timezonefinder>=8.2.0",
        "cdsapi>=0.7.7",
        "rainflow==3.2.0",
        "pybamm==26.6.2.0",
        "ruamel.yaml==0.19.1",
        "PyYAML==6.0.3",
    ],
    package_data={
        "": ["*.txt", "*.rst", "*.json", "*.jpg", "*.qss", "*.sh", "*.svg", "*.png", "*.kv", "*.bat", "*.csv", "*.md", "*.yml", "*.dll", "*.idf", "*.doctree", ".*info", "*.html", "*.js", "*.inv", "*.gif", "*.css", "*.eps", "*.pickle", "*.xlsx", "*.ttf", "*.pdf", "**/license*", "*.ui", "*.eot", "*.woff", "*.woff2", "LICENSE", "*.mplstyle", "*.ini"],
    },
    entry_points={
        "console_scripts": [
            "progress = progress.__main__:main",
        ],
    },
)
