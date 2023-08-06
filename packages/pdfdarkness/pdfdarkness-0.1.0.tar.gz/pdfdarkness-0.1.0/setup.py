from setuptools import setup, find_packages


setup(
    author="Hiroshi Matsuda",
    author_email="hmtd223@gmail.com",
    description="A command line tool for caluclating the darkness of the pages of PDF files",
    entry_points={
        "console_scripts": [
            "pdfdarkness = pdfdarkness.measure_darkness:main",
        ],
    },
    python_requires=">=3.6",
    install_requires=[
        "pdf2image>=1.16.0,<1.17.0",
    ],
    license="MIT License",
    name="pdfdarkness",
    packages=find_packages(include=["pdfdarkness"]),
    url="https://github.com/hiroshi-matsuda/pdfdarkness",
    version='0.1.0',
)
