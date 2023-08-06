import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

__version__ = "0.4.2"

setuptools.setup(
    name="molvis",
    version=__version__,
    author="Jon Kragskow",
    author_email="jonkragskow@gmail.com",
    description="A package for generating html scripts to visualise chemical structures using 3dmol.js",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/jonkragskow/molvis",
    project_urls={
        "Bug Tracker": "https://gitlab.com/jonkragskow/molvis/-/issues",
        "Documentation": "https://jonkragskow.gitlab.io/molvis"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "deprecation",
        "xyz_py"
    ],
    entry_points={
        'console_scripts': [
            'molvis = molvis.cli:main'
        ]
    }
)
