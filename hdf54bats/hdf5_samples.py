#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2018-2019 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from . import hdf5_base

class Hdf5Samples(hdf5_base.Hdf5Base):
    """ """
    def __init__(self, h5_path='', h5_name=None):
        """ """
        super().__init__(h5_path, h5_name)
    
    def add_sample(self, parent_id='', node_id='', title='', 
                   parent_sample_id='', item_type='sample',
                   metadata = {}):
        """ """
        if title == '':
            title = 'Sample: ' + node_id.capitalize().replace('_', ' ')
        # Sample group.
        new_id = self.create_group(parent_id=parent_id, 
                                   node_id=node_id, 
                                   item_title=title)
        # Metadata.
        metadata['item_type'] = item_type
        metadata['parent_sample_id'] = parent_sample_id
        self.set_user_metadata(new_id, metadata=metadata)
        #
        return new_id
    
    def remove_sample(self, item_id='', recursive=False):
        """ """
        self.remove(item_id=item_id, recursive=recursive)
    
    