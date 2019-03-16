#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2018-2019 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import pathlib
import tables
import hdf54bats

class Hdf5Base():
    """ Base functionality for a single HDF5 file. """
    
    def __init__(self, h5_path='', h5_name='hdf5'):
        """ """
        self.h5_path = pathlib.Path(h5_path, h5_name)
        if self.h5_path.suffix != '.h5':
            self.h5_path = self.h5_path.with_suffix('.h5')
        # The HDF5 file.
        self.h5 = None
    
    def open(self, read_only=True):
        """ """
        mode = 'r' if read_only else 'a'
        try:
            if self.h5 is None:
                self.h5 = tables.open_file(self.h5_path, mode)
        except Exception as e:
            print('Failed to open HDF5 file. Exception: ', e)
            self.h5 = None
    
    def close(self):
        """ """
        if self.h5 is not None:
            try:
                self.h5.close()
            finally:
                self.h5 = None
    
    def check_file(self):
        """ Checks if the file is a valid HDF5/PyTables file. """
        try:
            valid_file = tables.is_hdf5_file(self.h5_path)
            if valid_file:
                pytables_version = tables.is_pytables_file(self.h5_path)
                if pytables_version is None:
                    return False
                else:
                    return True
            else:
                return False
        except:
            return False
    
    def get_child_groups(self, item_id='', close=True):
        """ """
        groups_dict = {}
        item_id = '/' + item_id.replace('.', '/')
        item_id = item_id.replace('//', '/')
        try:
            self.open(read_only=True)
            for group in self.h5.walk_groups(item_id): 
                group_dict = {}
                group_dict['name'] = group._v_name
                item_id = group._v_pathname.strip('/') # Trim to root level.
                item_id = item_id.replace('/', '.')
                group_dict['item_id'] = item_id
                group_dict['item_title'] = group._v_attrs['TITLE']
                try: group_dict['item_type'] = group._v_attrs['item_type']
                except: group_dict['name'] = ''
                groups_dict[item_id] = group_dict
        finally:
            if close:
                self.close()
        return groups_dict       
    
    def get_child_nodes(self, item_id='', close=True):
        """ """
        nodes_dict = {}
        item_id = '/' + item_id.replace('.', '/')
        item_id = item_id.replace('//', '/')
        try:
            self.open(read_only=True)
            for node in self.h5.walk_nodes(item_id): 
                node_dict = {}
                node_dict['name'] = node._v_name
                item_id = node._v_pathname.strip('/') # Trim to root level.
                item_id = item_id.replace('/', '.')
                node_dict['item_id'] = item_id
                node_dict['item_title'] = node._v_attrs['TITLE']
                try: node_dict['item_type'] = node._v_attrs['item_type']
                except: node_dict['name'] = ''
                nodes_dict[item_id] = node_dict
        finally:
            if close:
                self.close()
        return nodes_dict       
    
    def get_item_title(self, item_id='', close=True):
        """ """
        item_title = ''
        item_id = '/' + item_id.replace('.', '/')
        item_id = item_id.replace('//', '/')
        try:
            self.open(read_only=True)
            node = self.h5.get_node(item_id)
            item_title = node._v_attrs['TITLE']
        finally:
            if close:
                self.close()
        return item_title       
    
    def create_group(self, parent_id='', new_group_name='', item_title='', close=True):
        """ """
        parent_id = '/' + parent_id.replace('.', '/')
        parent_id = parent_id.replace('//', '/')
        if new_group_name:
            new_group_name = hdf54bats.str_to_ascii(new_group_name)
        else:
            # Use title if name not given.
            new_group_name = hdf54bats.str_to_ascii(item_title)
        try:
            self.open(read_only=False)
            self.h5.create_group(parent_id, new_group_name, item_title, createparents=False)
        finally:
            if close:
                self.close()
        #
        new_id = parent_id + '/' + new_group_name
        return new_id.replace('/', '.')
    
    def add_array(self, parent_id, new_array_name='', array=None, 
                  item_title='', atom=None, close=True):
        """ """
        parent_id = '/' + parent_id.replace('.', '/')
        parent_id = parent_id.replace('//', '/')
        if new_array_name:
            new_array_name = hdf54bats.str_to_ascii(new_array_name)
        else:
            # Use title if name not given.
            new_array_name = hdf54bats.str_to_ascii(item_title)
        try:
            self.open(read_only=False)
            self.h5.create_array(parent_id, new_array_name, array, 
                                 title=item_title, atom=atom)
        finally:
            if close:
                self.close()
        #
        new_id = parent_id + '/' + new_array_name
        return new_id.replace('/', '.')
        
    def get_array(self, item_id='', close=True):
        """ """
        item_id = '/' + item_id.replace('.', '/')
        item_id = item_id.replace('//', '/')
        try:
            self.open(read_only=True)
            return self.h5.get_node(item_id)
        finally:
            if close:
                self.close()
        
#     def add_dataset(self, parent_id='', new_dataset_name='', item_title='', close=True):
#         """ """
#         parent_id = '/' + parent_id.replace('.', '/')
#         parent_id = parent_id.replace('//', '/')
#         if new_dataset_name:
#             new_dataset_name = hdf54bats.str_to_ascii(new_dataset_name)
#         else:
#             # Use title if name not given.
#             new_dataset_name = hdf54bats.str_to_ascii(item_title)
#         try:
#             self.open(read_only=False)
#              
#             # TODO:
#              
#         finally:
#             if close:
#                 self.close()
    
#     def add_table(self, parent_id='', new_table_name='', item_title='', close=True):
#         """ """
#         parent_id = '/' + parent_id.replace('.', '/')
#         if new_table_name:
#             new_table_name = hdf54bats.str_to_ascii(new_table_name)
#         else:
#             # Use title if name not given.
#             new_table_name = hdf54bats.str_to_ascii(item_title)
#         try:
#             self.open(read_only=False)
#              
#             # TODO:
#                          
#         finally:
#             if close:
#                 self.close()
    
    def get_user_metadata(self, item_id='', close=True):
        """ """
        metadata = {}
        item_id = '/' + item_id.replace('.', '/')
        item_id = item_id.replace('//', '/')
        try:
            self.open(read_only=True)
            node = self.h5.get_node(item_id)
            for key in node._v_attrs._f_list('user'):
                # print('DEBUG: Attribute: ', key, '   value: ', node._v_attrs[key])
                metadata[key] = node._v_attrs[key]
        finally:
            if close:
                self.close()
        return metadata
    
    def set_user_metadata(self, item_id, metadata={}, close=True):
        """ """
        item_id = '/' + item_id.replace('.', '/')
        item_id = item_id.replace('//', '/')
        try:
            self.open(read_only=False)
            node = self.h5.get_node(item_id)
            for key, value in metadata.items():
                node._v_attrs[key] = value
        finally:
            if close:
                self.close()
    
    def clear_user_metadata(self, item_id, close=True):
        """ """
        item_id = '/' + item_id.replace('.', '/')
        item_id = item_id.replace('//', '/')
        try:
            self.open(read_only=False)
            node = self.h5.get_node(item_id)
            for key in node._v_attrs._f_list('user'):
                self.h5.del_node_attr(node, key)
        finally:
            if close:
                self.close()
    
    def remove(self, item_id, recursive=False, close=True):
        """ Removes all types of nodes. """
        item_id = '/' + item_id.replace('.', '/')
        item_id = item_id.replace('//', '/')
        try:
            self.open(read_only=False)
            self.h5.remove_node(item_id, recursive=recursive)
        finally:
            if close:
                self.close()
    
