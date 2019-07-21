#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2018-2019 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import pathlib
import threading
import tables

class Hdf5Base():
    """ Base functionality for a single HDF5 file. """
    
    def __init__(self, h5_path='', h5_name='hdf5'):
        """ """
        self.h5_path = pathlib.Path(h5_path, h5_name)
        if self.h5_path.suffix != '.h5':
            self.h5_path = self.h5_path.with_suffix('.h5')
        # The HDF5 file.
        self.h5 = None
        # Lock used for concurrency reasons.
        self.lock = threading.Lock()
    
    def open(self, read_only=True):
        """ """
        mode = 'r' if read_only else 'a'
        try:
            if self.h5 is None:
                self.h5 = tables.open_file(str(self.h5_path), mode)
        except Exception as e:
            self.h5 = None
            print('Failed to open HDF5 file. Exception: ', e)
            raise
    
    def close(self):
        """ """
        try:
            try:
                if self.h5 is not None:
                    self.h5.close()
            finally:
                self.h5 = None
        except Exception as e:
            print('Failed to close HDF5 file. Exception: ', e)
            raise
    
    def check_file(self):
        """ Checks if the file is a valid HDF5/PyTables file. """
        self.lock.acquire(timeout=2)
        try:
            try:
                valid_file = tables.is_hdf5_file(str(self.h5_path))
                if valid_file:
                    pytables_version = tables.is_pytables_file(str(self.h5_path))
                    if pytables_version is None:
                        return False
                    else:
                        return True
                else:
                    return False
            except:
                return False
        finally:
            self.lock.release()
    
    def get_child_groups(self, node_id=''):
        """ """
        groups_dict = {}
        node_id = '/' + node_id.replace('.', '/')
        node_id = node_id.replace('//', '/')
        #
        self.lock.acquire(timeout=2)
        try:
            self.open(read_only=True)
            for group in self.h5.walk_groups(node_id): 
                group_dict = {}
                group_dict['name'] = group._v_name
                item_id = group._v_pathname.strip('/') # Trim to root level.
                item_id = item_id.replace('/', '.')
                group_dict['item_id'] = item_id
                group_dict['item_title'] = group._v_attrs['TITLE']
                try: group_dict['item_type'] = group._v_attrs['item_type']
                except: group_dict['name'] = ''
                groups_dict[item_id] = group_dict
            #
            return groups_dict
        finally:
            self.close()
            self.lock.release()
    
    def get_child_nodes(self, parent_id='', node_id=None):
        """ """
        nodes_dict = {}
        parent_id = '/' + parent_id.replace('.', '/')
        parent_id = parent_id.replace('//', '/')
        #
        self.lock.acquire(timeout=2)
        try:
            self.open(read_only=True)
            for node in self.h5.walk_nodes(parent_id, node_id): 
                node_dict = {}
                node_dict['name'] = node._v_name
                item_id = node._v_pathname.strip('/') # Trim to root level.
                item_id = item_id.replace('/', '.')
                node_dict['item_id'] = item_id
                node_dict['item_title'] = node._v_attrs['TITLE']
                try: node_dict['item_type'] = node._v_attrs['item_type']
                except: node_dict['name'] = ''
                nodes_dict[item_id] = node_dict
            return nodes_dict       
        finally:
            self.close()
            self.lock.release()
    
    def get_item_title(self, parent_id='', node_id=None):
        """ """
        item_title = ''
        parent_id = '/' + parent_id.replace('.', '/')
        parent_id = parent_id.replace('//', '/')
        #
        self.lock.acquire(timeout=2)
        try:
            self.open(read_only=True)
            node = self.h5.get_node(parent_id, node_id)
            item_title = node._v_attrs['TITLE']
            return item_title
        finally:
            self.close()
            self.lock.release()
    
    def create_group(self, parent_id='', node_id=None, item_title=''):
        """ """
        parent_id = '/' + parent_id.replace('.', '/')
        parent_id = parent_id.replace('//', '/')
        if node_id:
            new_id = parent_id + '/' + node_id
            new_id = new_id.replace('//', '/')
        #
        self.lock.acquire(timeout=2)
        try:
            self.open(read_only=False)
            self.h5.create_group(parent_id, node_id, item_title, createparents=False)
            #
            return new_id.replace('/', '.')
        finally:
            self.close()
            self.lock.release()
    
    def add_array(self, parent_id='', node_id=None, array=None, 
                  item_title='', atom=None):
        """ """
        parent_id = '/' + parent_id.replace('.', '/')
        parent_id = parent_id.replace('//', '/')
        if node_id:
            new_id = parent_id + '/' + node_id
            new_id = new_id.replace('//', '/')
        #
        self.lock.acquire(timeout=2)
        try:
            self.open(read_only=False)
            self.h5.create_array(parent_id, node_id, array, 
                                 title=item_title, atom=atom)
            #
            return new_id.replace('/', '.')
        finally:
            self.close()
            self.lock.release()
    
    def get_array(self, parent_id='', node_id=None):
        """ """
        parent_id = '/' + parent_id.replace('.', '/')
        parent_id = parent_id.replace('//', '/')
        #
        self.lock.acquire(timeout=2)
        try:
            self.open(read_only=True)
            array_object = self.h5.get_node(parent_id, node_id)
            return array_object.read()
        finally:
            self.close()
            self.lock.release()
    
    def get_user_metadata(self, parent_id='', node_id=None):
        """ """
        metadata = {}
        parent_id = '/' + parent_id.replace('.', '/')
        parent_id = parent_id.replace('//', '/')
        #
        self.lock.acquire(timeout=2)
        try:
            self.open(read_only=True)
            node = self.h5.get_node(parent_id, node_id)
            for key in node._v_attrs._f_list('user'):
                # print('DEBUG: Attribute: ', key, '   value: ', node._v_attrs[key])
                metadata[key] = node._v_attrs[key]
            #
            return metadata
        finally:
            self.close()
            self.lock.release()
    
    def set_user_metadata(self, parent_id='', node_id=None, metadata={}):
        """ """
        parent_id = '/' + parent_id.replace('.', '/')
        parent_id = parent_id.replace('//', '/')
        #
        self.lock.acquire(timeout=2)
        try:
            self.open(read_only=False)
            node = self.h5.get_node(parent_id, node_id)
            for key, value in metadata.items():
                node._v_attrs[key] = value
        finally:
            self.close()
            self.lock.release()
    
    def clear_user_metadata(self, parent_id='', node_id=None):
        """ """
        parent_id = '/' + parent_id.replace('.', '/')
        parent_id = parent_id.replace('//', '/')
        #
        self.lock.acquire(timeout=2)
        try:
            self.open(read_only=False)
            node = self.h5.get_node(parent_id, node_id)
            for key in node._v_attrs._f_list('user'):
                self.h5.del_node_attr(node, key)
        finally:
            self.close()
            self.lock.release()
    
    def exists(self, parent_id='', node_id=None):
        """ Checks if a node exists. """
        item_id = '/' + parent_id.replace('.', '/')
        if node_id:
            item_id = item_id + '/' + node_id
        item_id = item_id.replace('//', '/')
        #
        self.lock.acquire(timeout=2)
        try:
            self.open(read_only=False)
            exists = self.h5.__contains__(item_id)
            return exists
        finally:
            self.close()
            self.lock.release()
    
    def remove(self, parent_id='', node_id=None, recursive=False):
        """ Removes all types of nodes. """
        parent_id = '/' + parent_id.replace('.', '/')
        parent_id = parent_id.replace('//', '/')
        #
        self.lock.acquire(timeout=2)
        try:
            self.open(read_only=False)
            self.h5.remove_node(parent_id, node_id, recursive=recursive)
        finally:
            self.close()
            self.lock.release()
    
