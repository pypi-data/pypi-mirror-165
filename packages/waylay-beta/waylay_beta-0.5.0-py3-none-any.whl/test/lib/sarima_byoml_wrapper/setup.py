from setuptools import setup, find_packages

setup(
    name='sarima_byoml_wrapper',
    version='1.0',
    description='Custom Byoml wrapper for a statsmodels SARIMAX model',
    packages=find_packages(),
    install_requires=[
        'statsmodels==0.13.2',
        'dill',
        'pandas',
        'numpy',
    ]
)