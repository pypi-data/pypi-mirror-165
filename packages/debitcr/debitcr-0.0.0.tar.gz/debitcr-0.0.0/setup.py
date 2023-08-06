from setuptools import setup, find_packages

setup(
    name="debitcr",
    version='0.0.0',
    author="Norma Escobar",
    author_email="norma@normaescobar.com",
    packages=find_packages(),
    install_requires=['openpyxl', 'requests', 'json']
)