from setuptools import setup, find_packages

# from quest import __version__

DISTNAME = "ProGRESS"
VERSION = "1.2.0"
PYTHON_REQUIRES = ">=3.9, <3.12"
DESCRIPTION = "Probabilistic Grid Reliability Analysis with Energy Storage Systems"
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
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
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
        "plotly==5.22.0",
        "kaleido==0.2.1",
    ],

    package_data={
        '': ['*.txt', '*.rst', '*.json', '*.jpg', '*.qss', '*.sh', '*.svg', '*.png', '*.kv', '*.bat', '*.csv', '*.md', '*.yml', '*.dll', '*.idf', '*.doctree', '.*info', '*.html', '*.js', '*.inv', '*.gif', '*.css', '*.eps', '*.pickle', '*.xlsx', '*.ttf', '*.pdf', '**/license*', '*.yml', '*.ui', '*.eot', '*.woff', '*.woff2', 'LICENSE', '*.mplstyle', '*.ini' ],
    },

    entry_points={
        'console_scripts': [
            'progress = progress.__main__:main'
        ]
    }
)