# CloudedBats - HDF5

This is a part of CloudedBats: http://cloudedbats.org

## hdf54bats

The software library hdf54bats will be used to store data and metadata for bat monitoring projects and surveys. 

When working with large amounts of data it can be stored in the computer memory if it is in the range of Gigabytes of data. For surveys where many detectors are used that's not enough. For Terrabytes of data hard drives and solid state drives (SSD) can be used. Beyond that, when working with Petabytes of data, the solution is to store data in the Cloud. 

HDF5, Hierarchical Data Format, is a file format used to store and access huge amounts of data in an hierarchical manner. HDF5 uses the file system to store data and can therefore handle data in the Terrabyte range. In CloudedBats the Python library PyTables is used to handle the HDF5 storage.

## Installation

    virtualenv venv
    source venv/bin/activate
    pip install tables
    pip install h5py
    pip install git+https://github.com/cloudedbats/cloudedbats_hdf5
    
    python
    >>> import hdf54bats

## Contact

Arnold Andreasson, Sweden.

info@cloudedbats.org
