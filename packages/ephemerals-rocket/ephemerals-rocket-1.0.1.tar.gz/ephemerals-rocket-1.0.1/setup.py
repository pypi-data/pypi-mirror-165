import os
import pathlib
import setuptools

HERE = pathlib.Path(__file__).parent

LONG_DESCRIPTION = (HERE / "pypi.md").read_text()


REQUIREMENTS = [
    'requests>=2.28.1'
]


def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # Intentionally *not* adding an encoding option to open, See:
    # https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name="ephemerals-rocket",
    version=get_version("rocket/__init__.py"),
    author="Paranoid Software",
    author_email="info@paranoid.software",
    license="MIT",
    description="Ephemeral Rocket Database Context Helper.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url='https://github.com/paranoid-software/ephemerals.py/tree/main/rocket',
    packages=setuptools.find_packages(exclude=['tests*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIREMENTS,
    include_package_data=True,
    python_requires='>=3.6'
)
