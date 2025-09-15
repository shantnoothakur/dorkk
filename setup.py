from setuptools import setup, find_packages


setup(
name="advaitzz",
version="0.1.0",
description="ADVAITZZ - Interactive Google Dork Generator for legal recon",
author="ADVAITZZ",
packages=find_packages(),
include_package_data=True,
install_requires=[
"rich>=12.0.0",
"pandas>=1.0.0",
"click>=7.0"
],
entry_points={
'console_scripts': [
'advaitzz=advaitzz.cli:main'
]
},
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License'
]
)
