from setuptools import setup, find_packages

setup(
    name="codeclub",
    version='0.1',
    packages=find_packages(include=["codeclub", "codeclub.*"] + ["codeclub.puzzle.images"]),
    zip_safe=False,
    include_package_data=True
)