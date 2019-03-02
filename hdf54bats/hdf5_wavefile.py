#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2018-2019 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import numpy as np

from . import hdf5_base

class Hdf5Wavefile(hdf5_base.Hdf5Base):
    """ """
    def __init__(self, h5_path='', h5_name=None):
        """ """
        super().__init__(h5_path, h5_name)
    
    def get_wavefiles(self, from_top_node='', close=True):
        """ """
        wavefile_dict = {}
        try:
            self.open(read_only=True)
            # Events.
            event_nodes = self.get_children('', close=False)
            for event_node in event_nodes:
                # Detectors.
                node = event_node
                detector_nodes = self.get_children(node, close=False)
                for detector_node in detector_nodes:
                    # WaveFiles.
                    node = detector_node
                    wave_nodes = self.get_children(node, close=False)
                    for wave_node in wave_nodes:
                        title = self.get_title(wave_node)
                        if from_top_node: 
                            if wave_node.startswith(from_top_node):
                                wavefile_dict[wave_node] = title
                        else:
                            wavefile_dict[wave_node] = title
        finally:
            if close:
                self.close()
        #
        return wavefile_dict 
    
    def add_wavefile(self, parents='', name='', title='', array=np.arange(1), close=True):
        """ """
        if title == '':
            title = 'Wavefile: ' + name.capitalize().replace('_', ' ')
        #
#         atom_int16 = tables.Int16Atom()
        
        self.add_array(parents=parents, array_name=name, array_title=title, array=array, 
                       close=close, )
#                        atom=atom_int16)
        # Save to hdf5 file.
        if not close:
            self.h5.flush()
    
    def get_wavefile(self, nodepath='', close=True):
        """ """
        array_object = self.get_array(nodepath=nodepath, close=False, )
        array = array_object.read()
        #
        if close:
            self.close()
        return array
    
    def remove_wavefile(self, nodepath='', close=True):
        """ """
        self.remove(nodepath=nodepath, close=close, )
    
    def get_user_metadata(self, nodepath='', close=True):
        """ """
        return super().get_user_metadata(nodepath=nodepath, close=close, )
    
    def set_user_metadata(self, nodepath='', metadata={}, close=True):
        """ """
        super().set_user_metadata(nodepath=nodepath, metadata=metadata, close=close, )
    
    def clear_user_metadata(self, nodepath='', close=True):
        """ """
        super().clear_user_metadata(nodepath=nodepath, close=close, )
        
    