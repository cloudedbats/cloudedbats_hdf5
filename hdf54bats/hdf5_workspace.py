#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2018-2019 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import pathlib
import threading
import tables 

class Hdf5Workspace():
    """ This class handles the workspace (directory)
        where the HDF5/PyTables files are stored.
    """
    def __init__(self, workspace_path='workspace', create_ws=False):
        """ """
        self.workspace_path = workspace_path
        if create_ws:
            # Create workspace if it does not exist.
            ws_path = pathlib.Path(self.workspace_path)
            ws_path.mkdir(parents=True, exist_ok=True)
        #
        self.lock = threading.Lock()
    
    def get_h5_list(self):
        """ Returns a dictionary with filename as key. """
        h5_dict = {}
        self.lock.acquire(timeout=2)
        try:
            ws_path = pathlib.Path(self.workspace_path)
            for h5_file in ws_path.glob('*.h5'):
                filepath = pathlib.Path(h5_file).resolve()
                title = ''
                h5 = tables.open_file(str(h5_file), 'r')
                title = h5.get_node_attr('/', 'TITLE')
                h5_dict[h5_file.name] = {'name': h5_file.name, 
                                         'title': title, 
                                         'f5_filepath': filepath
                                        }
            return h5_dict
        finally:
            h5.close()
            self.lock.release()
    
    def get_h5_title(self, h5_name):
        """ Gets the survey title that corresponds to the file. """
        path = pathlib.Path(self.workspace_path, h5_name)
        #
        self.lock.acquire(timeout=2)
        try:
            h5 = tables.open_file(str(path), 'r')
            title = h5.get_node_attr('/', 'TITLE')
            return title
        finally:
            h5.close()
            self.lock.release()
    
    def set_h5_title(self, h5_name, title):
        """ Sets the survey title that corresponds to the file. """
        path = pathlib.Path(self.workspace_path, h5_name)
        #
        self.lock.acquire(timeout=2)
        try:
            h5 = tables.open_file(str(path), 'a')
            title = h5.set_node_attr('/', 'TITLE', title)
            return title
        finally:
            h5.close()
            self.lock.release()
    
    def check_h5_file(self, h5_name=None):
        """ Checks if it is a valid HDF5/PyTables file. """
        h5_path = pathlib.Path(self.workspace_path, h5_name)
        if h5_path.suffix != '.h5':
            h5_path = h5_path.with_suffix('.h5')
        try:
            valid_file = tables.is_hdf5_file(str(h5_path))
            if valid_file:
                pytables_version = tables.is_pytables_file(str(h5_path))
                if pytables_version is None:
                    return False
                else:
                    # print('DEBUG: PyTable version: ', pytables_version)
                    return True
            else:
                return False
        except:
            return False
    
    def create_h5(self, h5_name=None, title=''):
        """ Creats a new file representing a survey. """
        h5_path = pathlib.Path(self.workspace_path, h5_name)
        if h5_path.suffix != '.h5':
            h5_path = h5_path.with_suffix('.h5')
        #
        self.lock.acquire(timeout=2)
        h5 = tables.open_file(str(h5_path), "a")
        try:
            h5.set_node_attr('/', 'item_type', 'survey')
            if title:
                h5.set_node_attr('/', 'TITLE', title)
            else:
                # Generate title if not defined.
                title = 'Survey: ' + h5_name.capitalize().replace('_', ' ')
                h5.set_node_attr('/', 'TITLE', title)
        finally:
            h5.close()
            self.lock.release()
    
    def delete_h5(self, h5_name=None):
        """ Deleting a file. """
        h5_path = pathlib.Path(self.workspace_path, h5_name)
        if h5_path.suffix != '.h5':
            h5_path = h5_path.with_suffix('.h5')
        if h5_path.exists():
            h5_path.unlink()
    
    def copy_h5(self, from_h5_name=None, to_h5_name=None):
        """ Copies a file. Will reduce the size if content is removed. """
        h5_src = pathlib.Path(self.workspace_path, from_h5_name)
        if h5_src.suffix != '.h5':
            h5_src = h5_src.with_suffix('.h5')
        h5_dest = pathlib.Path(self.workspace_path, to_h5_name)
        if h5_dest.suffix != '.h5':
            h5_dest = h5_dest.with_suffix('.h5')
        #
        tables.copy_file(str(h5_src), str(h5_dest))
    
    def rename_h5(self, from_h5_name=None, to_h5_name=None):
        """ Renames a file. """
        h5_src = pathlib.Path(self.workspace_path, from_h5_name)
        if h5_src.suffix != '.h5':
            h5_src = h5_src.with_suffix('.h5')
        h5_dest = pathlib.Path(self.workspace_path, to_h5_name)
        if h5_dest.suffix != '.h5':
            h5_dest = h5_dest.with_suffix('.h5')
        #
        h5_src.rename(h5_dest)
    

### Test ###
# if __name__ == '__main__':
#     """ """
#     import time
#     print('\nCloudedBats - HDF5 - test')
#     ws = Hdf5Workspace(workspace_path='../workspace_test')
#     time.sleep(1)
#     ws.create_h5('h5_test')
#     time.sleep(1)
#     ws.copy_h5('h5_test', 'h5_test_1.h5')
#     time.sleep(1)
#     ws.rename_h5('h5_test_1', 'h5_test_2')
#     time.sleep(1)
#     print('\nCheck file: ')
#     print(' - Check: ', ws.check_h5_file('h5_test_2'))
#     print('\nBefore delete: ')
#     for filename in ws.get_h5_list():
#         print(' - ', filename)
#     time.sleep(1)
#     ws.delete_h5('h5_test')
#     time.sleep(1)
#     ws.delete_h5('h5_test_2.h5')
#     print('\nAfter delete: ')
#     for filename in ws.get_h5_list():
#         print(' - ', filename)

    