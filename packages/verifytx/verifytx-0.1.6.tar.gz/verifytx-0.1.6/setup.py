from setuptools import setup, find_packages

setup(
    name="verifytx",
    version='0.1.6',
    author="Norma Escobar",
    author_email="norma@normaescobar.com",
    packages=find_packages(),
    install_requires=['openpyxl', 'requests']
)