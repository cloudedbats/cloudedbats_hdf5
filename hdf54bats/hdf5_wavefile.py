#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2018 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import pathlib
import numpy as np
import tables 
import h5py 

from . import hdf5_base

class Hdf5Wavefile(hdf5_base.Hdf5Base):
    """ """
    def __init__(self, h5_path='', h5_name=None):
        """ """
        super().__init__(h5_path, h5_name)
    
    def get_wavefiles(self):
        """ """
        return[]
    
    def add_wavefile(self, parents='', name='', title='', array=np.arange(1)):
        """ """
        if title == '':
            title = 'Wavefile: ' + name.capitalize().replace('_', ' ')
        #
        self.add_array(parents=parents, node_name=name, node_title=title, array=array)
    
    def remove_wavefile(self, nodepath=''):
        """ """
        self.remove(nodepath=nodepath)
    
    def get_user_metadata(self, nodepath=''):
        """ """
        return super().get_user_metadata(nodepath=nodepath)
    
    def set_user_metadata(self, nodepath='', metadata={}):
        """ """
        super().set_user_metadata(nodepath=nodepath, metadata=metadata)
    
    def clear_user_metadata(self, nodepath=''):
        """ """
        super().clear_user_metadata(nodepath=nodepath)
        
    