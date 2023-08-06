""" This is a Python toolbox for hYPERspectral data. This toolbox includes methods for reading hyperspectral images and provides an interface for basic machine learning algorithms like decomposition and clustering.

A demo file can be found in the 'main.py' file.

This toolbox is devided into two packages

- chemometrics
    Package for creating datasets and preforming basic chemometrics analysises on them
- lab
    Package for managing data collected with the lab equiment and file structures from MeBioS.

Written by Remi Van Belleghem. Based on Matlab toolbox from Niels Wouters.

"""

# wavelength unit to be used in the entire package
WL_UNIT = 'nm'
WL_UNIT_LONG = 'nanometer'