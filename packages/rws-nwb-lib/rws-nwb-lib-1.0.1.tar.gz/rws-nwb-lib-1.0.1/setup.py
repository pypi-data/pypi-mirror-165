import re

import setuptools

# Versioning
VERSIONFILE = "rws_nwb_lib/__init__.py"
getversion = re.search(
    r"^__version__ = ['\"]([^'\"]*)['\"]", open(VERSIONFILE, "rt").read(), re.M
)

if getversion:
    new_version = getversion.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

# Setup
with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    install_requires=["geopandas", "requests", "pydantic"],
    tests_require=["pytest", "pytest-cov"],
    python_requires=">=3",
    name="rws-nwb-lib",
    version=new_version,
    author="Datalab",
    author_email="datalab.codebase@rws.nl",
    description="Library for automatically downloading the Dutch Nationaal Wegenbestand (NWB)",
    long_description=long_description + "\n\n",
    url="https://gitlab.com/rwsdatalab/public/codebase/tools/rws-nwb-lib",
    download_url="https://gitlab.com/rwsdatalab/public/codebase/tools/rws-nwb-lib/-/archive/"
    + new_version
    + ".tar.gz",
    packages=setuptools.find_packages(),  # Searches throughout all dirs for files to include
    include_package_data=True,  # Must be true to include files depicted in MANIFEST.in
    license="Apache Software License 2.0",
    license_files=["LICENSE"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    setup_requires=[
        # dependency for `python setup.py test`
        "pytest-runner",
        # dependencies for `python setup.py build_sphinx`
        "sphinx",
        "sphinxcontrib-pdfembed @ https://github.com/SuperKogito/sphinxcontrib-pdfembed",
        "sphinx_rtd_theme",
        "types-requests",
    ],
)
