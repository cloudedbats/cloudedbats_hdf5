from setuptools import setup

from hdf54bats import __version__

setup(name='hdf54bats',
    version=__version__,
    description='HDF5 for bats, a part of the CloudedBats.org project.',
    url='https://github.com/cloudedbats/cloudedbats_hdf5',
    author='Arnold Andreasson',
    author_email='info@cloudedbats.org',
    license='MIT',
    packages=['hdf54bats'],
    install_requires=[
        'numpy', 
        'pandas', 
        'h5py', 
        'pytables', 
    ],
    zip_safe=False)
