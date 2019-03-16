#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2018-2019 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from . import hdf5_base

class Hdf5Events(hdf5_base.Hdf5Base):
    """ """
    def __init__(self, h5_path='', h5_name=None):
        """ """
        super().__init__(h5_path, h5_name)
    
    def add_event(self, parent_id='', new_event_name='', 
                  item_type='event', parent_event_id='', 
                  title='', close=True):
        """ """
        if title == '':
            title = 'Event: ' + new_event_name.capitalize().replace('_', ' ')
        #
        try:
            new_id = self.create_group(parent_id=parent_id, 
                                       new_group_name=new_event_name, 
                                       item_title=title, close=False)
            metadata = {}
            metadata['item_type'] = item_type
            metadata['parent_event_id'] = parent_event_id
            self.set_user_metadata(new_id, metadata, close=False)
        finally:
            if close:
                self.close()
        #
        return new_id

    def remove_event(self, item_id='', recursive=False, close=True):
        """ """
        self.remove(item_id=item_id, recursive=recursive, close=close)
    