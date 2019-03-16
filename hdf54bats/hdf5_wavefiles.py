#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2018-2019 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import numpy as np

from . import hdf5_base

class Hdf5Wavefiles(hdf5_base.Hdf5Base):
    """ """
    def __init__(self, h5_path='', h5_name=None):
        """ """
        super().__init__(h5_path, h5_name)
    
#     def get_wavefiles(self, from_item_id='', close=True):
#         """ """
#         wavefile_dict = {}
#         try:
#             self.open(read_only=True)
#             # Events.
#             event_nodes = self.get_children('', close=False)
#             for event_node in event_nodes:
#                 # Detectors.
#                 node = event_node
#                 detector_nodes = self.get_children(node, close=False)
#                 for detector_node in detector_nodes:
#                     # WaveFiles.
#                     node = detector_node
#                     wave_nodes = self.get_children(node, close=False)
#                     for wave_node in wave_nodes:
#                         title = self.get_title(wave_node)
#                         if from_item_id: 
#                             if wave_node.startswith(from_item_id):
#                                 wavefile_dict[wave_node] = title
#                         else:
#                             wavefile_dict[wave_node] = title
#         finally:
#             if close:
#                 self.close()
#         #
#         return wavefile_dict 
    
    def add_wavefile(self, parent_id='', new_name='', 
                     item_type='wavefile', title='', 
                     array=np.arange(1), 
                     close=True):
        """ """
        if title == '':
            title = 'Wavefile: ' + new_name.capitalize().replace('_', ' ')
        #
        new_id = self.add_array(parent_id=parent_id, new_array_name=new_name, 
                                item_title=title, array=array, close=close, )
#                        atom=atom_int16)
        metadata = {}
        metadata['item_type'] = item_type
        self.set_user_metadata(new_id, metadata, close=close)
        # Save to hdf5 file.
        if not close:
            self.h5.flush()
        #
        return new_id
    
    def get_wavefile(self, item_id='', close=True):
        """ """
        array_object = self.get_array(item_id=item_id, close=False, )
        array = array_object.read()
        #
        if close:
            self.close()
        return array
    
    def remove_wavefile(self, item_id='', recursive=False, close=True):
        """ """
        self.remove(item_id=item_id, recursive=recursive, close=close)
    