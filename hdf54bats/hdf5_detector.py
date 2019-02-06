#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2018-2019 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import pathlib
import numpy as np
import tables 
import h5py 

from . import hdf5_base

class Hdf5Detector(hdf5_base.Hdf5Base):
    """ """
    def __init__(self, h5_path='', h5_name=None):
        """ """
        super().__init__(h5_path, h5_name)
    
    def get_detectors(self):
        """ """
        return[]
    
    def add_detector(self, parents='', name='', title=''):
        """ """
        if title == '':
            title = 'Detector: ' + name.capitalize().replace('_', ' ')
        #
        self.create_group(parents=parents, group_name=name, group_title=title)
    
    def remove_detector(self, nodepath=''):
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
    