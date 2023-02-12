import io
import os

import setuptools

# Package meta-data.
NAME = "pdflinkchecker"
DESCRIPTION = (
    "Code generator that produces a Python class from a YAML input file. "
    "Can be used to facilitate code completion for config objects. "
)
LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"
URL = "https://github.com/a-nau/pdf-link-checker"
EMAIL = "alex.code@mail.com"
AUTHOR = "Alexander Naumann"
REQUIRES_PYTHON = ">=3.7.0"

# Package requirements.
base_packages = [
    "PyPDF2==2.12.*",
    "tabulate",
]

dev_packages = base_packages + [
    "black>=20.1.0",
    "isort==5.9.3",
    "mypy>=0.761",
    "pre-commit>=2.9.2",
    "pytest>=4.5.0",
    "pytest-cov>=2.6.1",
    "pyupgrade>=3.2.0",
    # mypy
    "types-PyYAML",
]

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

# Load the package's __version__.py module as a dictionary.
about = {}
with open(os.path.join(here, NAME, "__version__.py")) as f:
    exec(f.read(), about)

# Where the magic happens:
setuptools.setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=setuptools.find_packages(),
    scripts=["bin/pdflinkchecker"],
    entry_points={
        "console_scripts": [
            "pdflinkchecker = pdflinkchecker:check"
        ]
    },
    install_requires=base_packages,
    extras_require={"dev": dev_packages,},
    include_package_data=True,
    license="MIT",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    ext_modules=[],
)
