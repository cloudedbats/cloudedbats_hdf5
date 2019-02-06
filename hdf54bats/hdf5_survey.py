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

class Hdf5Survey(hdf5_base.Hdf5Base):
    """ """
    def __init__(self, h5_path='', h5_name=None):
        """ """
        super().__init__(h5_path, h5_name)
    
    def get_surveys(self):
        """ """
        return[]
    
    def add_survey(self, parents='', name='', title=''):
        """ 
            Note: Since there is one survey in each file all survey data is stored
            in the root group.
        """ 
        if title == '':
            title = 'Survey: ' + name.capitalize().replace('_', ' ')
        #
        self.create_group(parents=parents, node_name=name, node_title=title)
    
    def remove_survey(self, nodepath=''):
        """ 
            Note: Since there is one survey in each file all survey data is stored
            in the root group.
            
        """
        ### self.remove(nodepath=nodepath)
    
    def get_user_metadata(self, nodepath=''):
        """ """
        return super().get_user_metadata(nodepath=nodepath)
    
    def set_user_metadata(self, nodepath='', metadata={}):
        """ """
        super().set_user_metadata(nodepath=nodepath, metadata=metadata)
    
    def clear_user_metadata(self, nodepath=''):
        """ """
        super().clear_user_metadata(nodepath=nodepath)
    