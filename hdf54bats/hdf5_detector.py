#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2018-2019 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from . import hdf5_base

class Hdf5Detector(hdf5_base.Hdf5Base):
    """ """
    def __init__(self, h5_path='', h5_name=None):
        """ """
        super().__init__(h5_path, h5_name)
    
    def get_detectors(self, close=True):
        """ """
        return[]
    
    def add_detector(self, parents='', name='', title='', close=True):
        """ """
        if title == '':
            title = 'Detector: ' + name.capitalize().replace('_', ' ')
        #
        self.create_group(parents=parents, group_name=name, group_title=title, close=close)
    
    def remove_detector(self, nodepath='', close=True):
        """ """
        self.remove(nodepath=nodepath, close=close)
    
    def get_user_metadata(self, nodepath='', close=True):
        """ """
        return super().get_user_metadata(nodepath=nodepath, close=close)
    
    def set_user_metadata(self, nodepath='', metadata={}, close=True):
        """ """
        super().set_user_metadata(nodepath=nodepath, metadata=metadata, close=close)
    
    def clear_user_metadata(self, nodepath='', close=True):
        """ """
        super().clear_user_metadata(nodepath=nodepath, close=close)
    