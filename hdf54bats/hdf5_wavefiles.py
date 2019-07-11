#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2018-2019 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import numpy
import tables

from . import hdf5_samples

class Hdf5Wavefiles(hdf5_samples.Hdf5Samples):
    """ """
    def __init__(self, h5_path='', h5_name=None):
        """ """
        super().__init__(h5_path, h5_name)
    
    def add_wavefile(self, parent_id='', new_name='', title='', 
                     parent_sample_id='', item_type='wavefile', 
                     array=numpy.arange(1), 
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
    
    
    
    
    def add_pulse_peaks_table(self, wavefile_id, result_table):
        """ """
        wavefile_id = '/' + wavefile_id.replace('.', '/')
        wavefile_id = wavefile_id.replace('//', '/')
        try:
            self.open(read_only=False)
            # 
            try:
                self.h5.remove_node(wavefile_id, 'pulse_peaks')
            except:
                pass # Normal if it does not exist.
            # 
            expectedrows = len(result_table)
            table = self.h5.create_table(wavefile_id, 'pulse_peaks', PulsePeaks, 
                                         expectedrows=expectedrows)
            table_row = table.row
            # 
            for row in result_table:
                table_row['type'] = row[0]
                table_row['time_s'] = float(row[1])
                table_row['freq_khz'] = float(row[2])
                table_row['amp_dbfs'] = float(row[3])
                table_row['pulse_ix'] = int(row[4])
                table_row['info_key'] = row[5]
                table_row['info_value'] = row[6]
                # 
                table_row.append()
                # 
            table.flush
            # 
        finally:
            self.close()
    
    def get_pulse_peaks_table(self, wavefile_id='', close=True):
        """ """
        table_id = '/' + wavefile_id.replace('.', '/') + '/pulse_peaks'
        table_id = table_id.replace('//', '/')
        try:
            self.open(read_only=True)
            table =  self.h5.get_node(table_id)
            
#             test_arr = [ table_row['type'] for table_row in table ]
#             print(test_arr)
#             test_arr = [ table_row['time_s'] for table_row in table ]
#             print(test_arr)
#             test_arr = [ table_row['amp_dbfs'] for table_row in table ]
#             print(test_arr)
            
            result_dict = {}
            
#             result_dict['type'] = []
            result_dict['time_s'] = [ table_row['time_s'] for table_row in table 
                                      if table_row['type'] == b'1' and table_row['amp_dbfs'] > -100.0 ]
            result_dict['freq_khz'] = [ table_row['freq_khz'] for table_row in table 
                                      if table_row['type'] == b'1' and table_row['amp_dbfs'] > -100.0 ]
            result_dict['amp_dbfs'] = [ table_row['amp_dbfs'] for table_row in table 
                                      if table_row['type'] == b'1' and table_row['amp_dbfs'] > -100.0 ]
#             result_dict['pulse_ix'] = []
#             result_dict['info_key'] = []
#             result_dict['info_value'] = []
            #
            return result_dict
        
        finally:
            if close:
                self.close()
    
    
    

class PulsePeaks(tables.IsDescription):
    """ 
        Header: 'type', 'time_s', 'freq_khz', 'amp_dbfs', 'pulse_ix', 'info_key', 'info_value'
    """
    type = tables.StringCol(itemsize=5, dflt='', pos = 0)
    time_s = tables.Float32Col(dflt=numpy.nan, pos=1)
    freq_khz = tables.Float32Col(dflt=numpy.nan, pos=2)
    amp_dbfs = tables.Float32Col(dflt=numpy.nan, pos=3)
    pulse_ix = tables.UInt16Col(pos=4)
    # Used if type='info'.
    info_key = tables.StringCol(itemsize=32, dflt='', pos=5)
    info_value = tables.StringCol(itemsize=128, dflt='', pos=6)
    
    
    
