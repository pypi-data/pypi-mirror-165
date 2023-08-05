from setuptools import setup, find_packages
import pypandoc

long_description = pypandoc.convert_file('README.md', 'rst')

setup(
    name='peaktemp',
    version='0.2.2',
    license='MIT',
    author="Jake Hofgard",
    author_email='whofgard@stanford.edu',
    packages=find_packages('peaktemp'),
    package_dir={'': 'peaktemp'},
    url='https://github.com/jakehofgard/peaktemp',
    keywords='climate, temperature, forecasting, peak load',
    python_requires='>=3.8',
    description="Implementation of the Western Interstate Energy Board's peak temperature forecasting tool, using CMIP6 climate projection models from the Copernicus Climate Data Store (CDS) and NOAA's Integrated Surface Database (ISD).",
    long_description=long_description,
    install_requires=[
        'matplotlib',
        'pandas',
        'numpy',
        'seaborn',
        'cdsapi',
        'xarray',
        'xgboost',
        'scikit-learn',
        'datetime',
        'geopy'
    ],
)
