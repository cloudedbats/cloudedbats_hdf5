#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2018 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import pathlib
import tables 

class Hdf5Workspace():
    """ This class handles the workspace (directory)
        where the HDF5/PyTables files are stored.
    """
    def __init__(self, workspace_path='hdf5_workspace'):
        """ """
        self.workspace_path = workspace_path
        # Create workspace if it does not exist.
        ws_path = pathlib.Path(self.workspace_path)
        ws_path.mkdir(parents=True, exist_ok=True)
    
    def get_hdf5_list(self):
        """ """
        h5_list = []
        ws_path = pathlib.Path(self.workspace_path)
        for h5_file in ws_path.glob('*.h5'):
            # print(h5_file)
            h5_list.append(h5_file.name)
        return h5_list
    
    def check_hdf5_file(self, h5_name=None):
        """ """
        h5_path = pathlib.Path(self.workspace_path, h5_name)
        if h5_path.suffix != '.h5':
            h5_path = h5_path.with_suffix('.h5')
        try:
            valid_file = tables.is_hdf5_file(h5_path)
            if valid_file:
                pytables_version = tables.is_pytables_file(h5_path)
                if pytables_version is None:
                    return False
                else:
                    # print('DEBUG: PyTable version: ', pytables_version)
                    return True
            else:
                return False
        except:
            return False
    
    def create_hdf5(self, h5_name=None):
        """ """
        h5_path = pathlib.Path(self.workspace_path, h5_name)
        if h5_path.suffix != '.h5':
            h5_path = h5_path.with_suffix('.h5')
        h5 = tables.open_file(h5_path, "w")
        h5.close()
    
    def delete_hdf5(self, h5_name=None):
        """ """
        h5_path = pathlib.Path(self.workspace_path, h5_name)
        if h5_path.suffix != '.h5':
            h5_path = h5_path.with_suffix('.h5')
        if h5_path.exists():
            h5_path.unlink()
    
    def copy_hdf5(self, from_h5_name=None, to_h5_name=None):
        """ """
        h5_src = pathlib.Path(self.workspace_path, from_h5_name)
        if h5_src.suffix != '.h5':
            h5_src = h5_src.with_suffix('.h5')
        h5_dest = pathlib.Path(self.workspace_path, to_h5_name)
        if h5_dest.suffix != '.h5':
            h5_dest = h5_dest.with_suffix('.h5')
        #
        h5_dest.write_bytes(h5_src.read_bytes())
    
    def rename_hdf5(self, from_h5_name=None, to_h5_name=None):
        """ """
        h5_src = pathlib.Path(self.workspace_path, from_h5_name)
        if h5_src.suffix != '.h5':
            h5_src = h5_src.with_suffix('.h5')
        h5_dest = pathlib.Path(self.workspace_path, to_h5_name)
        if h5_dest.suffix != '.h5':
            h5_dest = h5_dest.with_suffix('.h5')
        #
        h5_src.rename(h5_dest)
    

### Test ###
if __name__ == '__main__':
    """ """
    import time
    print('\nCloudedBats - HDF5 - test')
    ws = Hdf5Workspace(workspace_path='../workspace_test')
    time.sleep(1)
    ws.create_hdf5('h5_test')
    time.sleep(1)
    ws.copy_hdf5('h5_test', 'h5_test_1.hdf5')
    time.sleep(1)
    ws.rename_hdf5('h5_test_1', 'h5_test_2')
    time.sleep(1)
    print('\nCheck file: ')
    print(' - Check: ', ws.check_hdf5_file('h5_test_2'))
    print('\nBefore delete: ')
    for filename in ws.get_hdf5_list():
        print(' - ', filename)
    time.sleep(1)
    ws.delete_hdf5('h5_test')
    time.sleep(1)
    ws.delete_hdf5('h5_test_2.hdf5')
    print('\nAfter delete: ')
    for filename in ws.get_hdf5_list():
        print(' - ', filename)

    