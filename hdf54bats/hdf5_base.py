#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2018 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import pathlib
# import numpy as np
import tables 
# import h5py 

class Hdf5Base():
    """ Base functionality for a single HDF5 file. """
    
    def __init__(self, h5_path='', h5_name=None):
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
            self.h5 = tables.open_file(self.h5_path, mode)
        except:
            self.h5 = None
    
    def close(self):
        """ """
        if self.h5 is not None:
            try:
                self.h5.close()
            finally:
                self.h5 = None
    
    def check_file(self):
        """ Check if the file is a valid HDF5/PyTables file. """
        try:
            valid_file = tables.is_hdf5_file(self.h5_path)
            if valid_file:
                pytables_version = tables.is_pytables_file(self.h5_path)
                if pytables_version is None:
                    return False
                else:
                    # print('DEBUG: PyTable version: ', pytables_version)
                    return True
            else:
                return False
        except:
            return False
    
    def get_children(self, nodepath=''):
        """ """
        node_list = []
        nodepath = '/' + nodepath.replace('.', '/')
        try:
            self.open(read_only=True)
            nodes = self.h5.list_nodes(nodepath)
            for node_name in nodes:
                nodes = str(node_name).split(' ')[0]
                nodes = nodes.replace('/', '.')[1:]
                node_list.append(nodes)
                print('DEBUG: node: ', node_name, '   First part:', nodes)
        finally:
            self.close()
        return node_list       
    
    def create_group(self, parents='', node_name='', node_title=''):
        """ """
        parents = '/' + parents.replace('.', '/')
        node_name = node_name.replace(' ', '_').lower()
        try:
            self.open(read_only=False)
            self.h5.create_group(parents, node_name, node_title, createparents=False)
        finally:
            self.close()
    
    def add_dataset(self, parents='', node_name='', node_title=''):
        """ """
        parents = '/' + parents.replace('.', '/')
        node_name = node_name.replace(' ', '_').lower()
        try:
            self.open(read_only=False)
            
            # TODO:
            
        finally:
            self.close()
    
    def add_array(self, parents='', node_name='', node_title='', array=None):
        """ """
        parents = '/' + parents.replace('.', '/')
        node_name = node_name.replace(' ', '_').lower()
        try:
            self.open(read_only=False)
            self.h5.create_array(parents, node_name, array, title=node_title)
        finally:
            self.close()
        
    def add_table(self, parents='', node_name='', node_title=''):
        """ """
        parents = '/' + parents.replace('.', '/')
        node_name = node_name.replace(' ', '_').lower()
        try:
            self.open(read_only=False)
            
            # TODO:
                        
        finally:
            self.close()
    
    def get_user_metadata(self, nodepath='', node_name=''):
        """ """
        metadata = {}
        nodepath = '/' + nodepath.replace('.', '/')
        try:
            self.open(read_only=False)
            node = self.h5.get_node(nodepath)
            for key in node._v_attrs._f_list('user'):
                # print('DEBUG: Attribute: ', key, '   value: ', node._v_attrs[key])
                metadata[key] = node._v_attrs[key]
        finally:
            self.close()
        return metadata
    
    def set_user_metadata(self, nodepath, metadata={}):
        """ """
        nodepath = '/' + nodepath.replace('.', '/')
        try:
            self.open(read_only=False)
            node = self.h5.get_node(nodepath)
            for key, value in metadata.items():
                node._v_attrs[key] = value
        finally:
            self.close()
    
    def clear_user_metadata(self, nodepath):
        """ """
        nodepath = '/' + nodepath.replace('.', '/')
        try:
            self.open(read_only=False)
            node = self.h5.get_node(nodepath)
            for key in node._v_attrs._f_list('user'):
                self.h5.del_node_attr(node, key)
#                 node._v_attrs(key)._g_remove()
        finally:
            self.close()
    
    def remove(self, nodepath):
        """ Removes all types of nodes. """
        nodepath = '/' + nodepath.replace('.', '/')
        try:
            self.open(read_only=False)
            self.h5.remove_node(nodepath, recursive=True)
        finally:
            self.close()
    
