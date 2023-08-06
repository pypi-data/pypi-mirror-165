# Calibration transfer for chemometrics and spectral data applications

This package contains methods to perform calibration transfer based on bilinear models, mainly Partial Least Squares Regression.
Numpy and Sci-Kit Learn are mandatory dependencies

The methods included are:

(Piecewise) Direct standardization (PDS, DS) (Wang 1991, Bouveresse1996)

Orthogonal projection (EPO transfer) (Zeaiter 2006, Roger 2003)

Domain invariant PLS (Nikzad-Langerodi 2018, 2020)

Joint Y PLS (Folch-Fortuny 2017, Garcia Munoz 2005)

Spectral Space Transformation (SST) (W. Du, 2011)

Transfer by orthogonal projection (TOP) (A. Andrew and T. Fearn, 2004)

Dynamic orthogonal projection (DOP) (Zeater, et al 2006)

Transfer component analysis (TCA) (Pan, et at 2011)

Unsupervised dynamic orthogonal projection (uDOP) (Fonseca Diaz, et al 2022)


## Installation options

### Option 1. Install via pip

```python
pip install pycaltransfer
```

### Option 2. Clone repository

```git
git clone https://gitlab.com/chemosoftware/python/pycaltransfer.git
```

To start using this package and get the documentation of the methods, do:

```python
import pycaltransfer.caltransfer as caltransfer
help(caltransfer.ds_pc_transfer_fit)
help(caltransfer.pds_pls_transfer_fit)
help(caltransfer.epo_fit)
help(caltransfer.jointypls_regression)
help(caltransfer.slope_bias_correction)
help(caltransfer.dipals)
help(caltransfer.sst)
help(caltransfer.top)
help(caltransfer.dop)
help(caltransfer.linear_tca)
help(caltransfer.udop)
```
