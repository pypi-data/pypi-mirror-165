from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1.0'
DESCRIPTION = 'Predticts Basmati Paddy Seeds '

# Setting up
setup(
    name="iRSVPred_2",
    version=VERSION,
    author="Nimisha_Tiwari",
    author_email="nimi.tiwari08@gmail.com",
    include_package_data=True,
    package_data= { 'simple' : ['Rice_InResv2_Aug36_25epochs.h5']},
     
    description=DESCRIPTION,
    packages=['iRSVPred_2'],
    install_requires=['opencv-python', 'tensorflow', 'keras', 'numpy','matplotlib',],
    keywords=['python', 'Rice', 'Basmati', 'deep learning', 'image classification', 'icgeb'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
