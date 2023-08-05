from setuptools import setup, find_packages


import codecs
import os.path


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


with open("README.md") as readme_file:
    readme = readme_file.read()


test_deps = (["pytest", "coverage"],)
extra_deps = {"test": test_deps}

setup(
    author="Thomas Mohren",
    author_email="tlmohren@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Data writers with optional timestamps for logging of events",
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    name="event_data_logging",
    packages=["event_data_logging"],
    test_suite="tests",
    install_requires=["numpy"],
    tests_require=test_deps,
    extras_require=extra_deps,
    package_dir={"": "src"},
    url="https://github.com/maimonlab/event_data_logging",
    # version=version,
    version=get_version("src/event_data_logging/__init__.py"),
    zip_safe=False,
)

# keywords="python_boilerplate",
# packages=find_packages(include=["python_boilerplate", "python_boilerplate.*"]),
# packages=find_packages(where="src"),
# package_data=[]
