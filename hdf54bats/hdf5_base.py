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
    
    def get_children(self, nodepath='', close=True):
        """ """
        node_list = []
        nodepath = '/' + nodepath.replace('.', '/')
        nodepath = nodepath.replace('//', '/')
        try:
            self.open(read_only=True)
            nodes = self.h5.list_nodes(nodepath)
            for node_name in nodes:
                nodes = str(node_name).split(' ')[0]
                nodes = nodes.replace('/', '.')[1:]
                node_list.append(nodes)
                print('DEBUG: node: ', node_name, '   First part:', nodes)
        finally:
            if close:
                self.close()
        return node_list       
    
    def get_title(self, nodepath='', close=True):
        """ """
        title = ''
        nodepath = '/' + nodepath.replace('.', '/')
        nodepath = nodepath.replace('//', '/')
        try:
            self.open(read_only=True)
            node = self.h5.get_node(nodepath)
            title = node._v_attrs['TITLE']
        finally:
            if close:
                self.close()
        return title       
    
    def create_group(self, parents='', group_name='', group_title='', close=True):
        """ """
        parents = '/' + parents.replace('.', '/')
        parents = parents.replace('//', '/')
        if group_name:
            group_name = hdf54bats.str_to_ascii(group_name)
        else:
            group_name = hdf54bats.str_to_ascii(group_title)
        try:
            self.open(read_only=False)
            self.h5.create_group(parents, group_name, group_title, createparents=False)
        finally:
            if close:
                self.close()
    
    def add_array(self, parents='', array_name='', array=None, 
                  array_title='', atom=None, close=True):
        """ """
        parents = '/' + parents.replace('.', '/')
        parents = parents.replace('//', '/')
        if array_name:
            array_name = hdf54bats.str_to_ascii(array_name)
        else:
            array_name = hdf54bats.str_to_ascii(array_title)
        try:
            self.open(read_only=False)
            self.h5.create_array(parents, array_name, array, 
                                 title=array_title, atom=atom)
        finally:
            if close:
                self.close()
        
    def get_array(self, nodepath='', close=True):
        """ """
        nodepath = '/' + nodepath.replace('.', '/')
        nodepath = nodepath.replace('//', '/')
        try:
            self.open(read_only=True)
            return self.h5.get_node(nodepath)
        finally:
            if close:
                self.close()
        
    def add_dataset(self, parents='', dataset_name='', dataset_title='', close=True):
        """ """
        parents = '/' + parents.replace('.', '/')
        parents = parents.replace('//', '/')
        if dataset_name:
            dataset_name = hdf54bats.str_to_ascii(dataset_name)
        else:
            dataset_name = hdf54bats.str_to_ascii(dataset_title)
        try:
            self.open(read_only=False)
            
            # TODO:
            
        finally:
            if close:
                self.close()
    
    def add_table(self, parents='', table_name='', table_title='', close=True):
        """ """
        parents = '/' + parents.replace('.', '/')
        if table_name:
            table_name = hdf54bats.str_to_ascii(table_name)
        else:
            table_name = hdf54bats.str_to_ascii(table_title)
        try:
            self.open(read_only=False)
            
            # TODO:
                        
        finally:
            if close:
                self.close()
    
    def get_user_metadata(self, nodepath='', close=True):
        """ """
        metadata = {}
        nodepath = '/' + nodepath.replace('.', '/')
        nodepath = nodepath.replace('//', '/')
        try:
            self.open(read_only=True)
            node = self.h5.get_node(nodepath)
            for key in node._v_attrs._f_list('user'):
                # print('DEBUG: Attribute: ', key, '   value: ', node._v_attrs[key])
                metadata[key] = node._v_attrs[key]
        finally:
            if close:
                self.close()
        return metadata
    
    def set_user_metadata(self, nodepath, metadata={}, close=True):
        """ """
        nodepath = '/' + nodepath.replace('.', '/')
        nodepath = nodepath.replace('//', '/')
        try:
            self.open(read_only=False)
            node = self.h5.get_node(nodepath)
            for key, value in metadata.items():
                node._v_attrs[key] = value
        finally:
            if close:
                self.close()
    
    def clear_user_metadata(self, nodepath, close=True):
        """ """
        nodepath = '/' + nodepath.replace('.', '/')
        nodepath = nodepath.replace('//', '/')
        try:
            self.open(read_only=False)
            node = self.h5.get_node(nodepath)
            for key in node._v_attrs._f_list('user'):
                self.h5.del_node_attr(node, key)
#                 node._v_attrs(key)._g_remove()
        finally:
            if close:
                self.close()
    
    def remove(self, nodepath, recursive=False, close=True):
        """ Removes all types of nodes. """
        nodepath = '/' + nodepath.replace('.', '/')
        nodepath = nodepath.replace('//', '/')
        try:
            self.open(read_only=False)
            self.h5.remove_node(nodepath, recursive=recursive)
        finally:
            if close:
                self.close()
    
