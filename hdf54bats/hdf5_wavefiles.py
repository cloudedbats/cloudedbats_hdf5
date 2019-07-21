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
    
    def add_wavefile(self, parent_id='', node_id='', title='', 
                     parent_sample_id='', item_type='wavefile', 
                     array=numpy.arange(1),
                     metadata = {}):
        """ """
        if title == '':
            title = 'Wavefile: ' + node_id.capitalize().replace('_', ' ')
        # Add sample of type wavefile first.
        new_id = super().add_sample(parent_id, node_id, title, 
                                    parent_sample_id=parent_sample_id, 
                                    item_type=item_type)
        # Then add the signal array to the sample.
        self.add_array(parent_id=new_id, node_id='signal', 
                       item_title=title, array=array)
        # Metadata.
        metadata['item_type'] = item_type
        self.set_user_metadata(new_id, metadata=metadata)
        #
        return new_id
    
    def get_wavefile(self, wavefile_id=''):
        """ """
        array = self.get_array(parent_id=wavefile_id, node_id='signal')
        #
        return array
    
    def remove_wavefile(self, wavefile_id='', recursive=True):
        """ """
        self.remove(parent_id=wavefile_id, recursive=recursive)
    
    def add_wavefile_peaks(self, wavefile_id, result_table,
                              metadata = {}):
        """ """
        wavefile_id = '/' + wavefile_id.replace('.', '/')
        wavefile_id = wavefile_id.replace('//', '/')
        wavefile_peaks_id = wavefile_id + '/wavefile_peaks'
        # Remove old, if exists.
        if self.exists(wavefile_peaks_id):
            self.remove(wavefile_peaks_id)
        # Array.
        new_array = []
        for row in result_table:
            new_array.append([float(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4])])
        #
        self.add_array(parent_id=wavefile_id, node_id='wavefile_peaks', array=new_array)
        # Metadata.
        metadata['item_type'] = 'wavefile_peaks'
        self.set_user_metadata(wavefile_peaks_id, metadata=metadata)
    
    def get_wavefile_peaks(self, wavefile_id=''):
        """ """
        wavefile_id = '/' + wavefile_id.replace('.', '/')
        wavefile_id = wavefile_id.replace('//', '/')
        #
        wavefile_peaks = self.get_array(parent_id=wavefile_id, node_id='wavefile_peaks')
        #
        result_dict = {}
        result_dict['type'] = []
        result_dict['time_s'] = []
        result_dict['freq_khz'] = []
        result_dict['amp_dbfs'] = []
        result_dict['pulse_ix'] = []
        for table_row in wavefile_peaks:
            if table_row[0] == 1.0:
                if table_row[3] > -100.0:
                    result_dict['type'].append(table_row[0])
                    result_dict['time_s'].append(table_row[1])
                    result_dict['freq_khz'].append(table_row[2])
                    result_dict['amp_dbfs'].append(table_row[3])
                    result_dict['pulse_ix'].append(table_row[4])
        #
        return result_dict


# TODO: Remove, not used. Results in 'segmentation faults':
#
# class PulsePeaks(tables.IsDescription):
#     """ Header: 'type', 'time_s', 'freq_khz', 'amp_dbfs', 'pulse_ix', 'info_key', 'info_value'
#     """
#     type = tables.StringCol(itemsize=5, dflt='', pos = 0)
#     time_s = tables.Float32Col(dflt=numpy.nan, pos=1)
#     freq_khz = tables.Float32Col(dflt=numpy.nan, pos=2)
#     amp_dbfs = tables.Float32Col(dflt=numpy.nan, pos=3)
#     pulse_ix = tables.UInt16Col(pos=4)
#     # Used if type='info'.
#     info_key = tables.StringCol(itemsize=32, dflt='', pos=5)
#     info_value = tables.StringCol(itemsize=128, dflt='', pos=6)
    
    
    
