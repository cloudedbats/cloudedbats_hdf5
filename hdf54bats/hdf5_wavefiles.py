#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2018-2019 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import numpy as np

from . import hdf5_samples

class Hdf5Wavefiles(hdf5_samples.Hdf5Samples):
    """ """
    def __init__(self, h5_path='', h5_name=None):
        """ """
        super().__init__(h5_path, h5_name)
    
    def add_wavefile(self, parent_id='', new_name='', title='', 
                     parent_sample_id='', item_type='wavefile', 
                     array=np.arange(1), 
                     close=True):
        """ """
        try:
            if title == '':
                title = 'Wavefile: ' + new_name.capitalize().replace('_', ' ')
            # Add sample of type wavefile first.
            new_id = super().add_sample(parent_id, new_name, title, 
                                        parent_sample_id=parent_sample_id, 
                                        item_type=item_type, close=False)
            # Then add the signal array to the sample.
            self.add_array(parent_id=new_id, new_array_name='signal', 
                           item_title=title, array=array, close=False)
    #                        atom=atom_int16)
            metadata = {}
            metadata['item_type'] = item_type
            self.set_user_metadata(new_id, metadata, close=False)
            # Save to hdf5 file.
        finally:
            if close:
                self.close()
        # Flush the array if not closed.
        if not close:
            self.h5.flush()
        #
        return new_id
    
    def get_wavefile(self, item_id='', close=True):
        """ """
        item_id = item_id + '.signal'
        array_object = self.get_array(item_id=item_id, close=False, )
        array = array_object.read()
        #
        if close:
            self.close()
        return array
    
    def remove_wavefile(self, item_id='', recursive=True, close=True):
        """ """
        self.remove(item_id=item_id, recursive=recursive, close=close)
    