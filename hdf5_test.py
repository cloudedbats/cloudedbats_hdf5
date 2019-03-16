#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2018-2019 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

# Library: hdf54bats, HDF5 for bats.
# Test during development. 

import numpy as np
import hdf54bats

ws = hdf54bats.Hdf5Workspace('workspace_test', create_ws=True)
ws.delete_h5('first_test')
ws.create_h5('first_test') # Not mandatory, will be created later.


survey = hdf54bats.Hdf5Survey('workspace_test', 'first_test')
# survey.add_survey('', 'first_survey')
# survey.add_survey('', 'dummy', 'DUMMY')
# survey.remove_survey('dummy')

events = hdf54bats.Hdf5Events('workspace_test', 'first_test')
events.add_event('', 'first_event')
events.add_event('', 'dummy', 'DUMMY')
events.remove_event('dummy')
 
samples = hdf54bats.Hdf5Samples('workspace_test', 'first_test')
samples.add_sample('first_event', 'wurb1')
samples.add_sample('first_event', 'dummy', 'DUMMY')
samples.remove_sample('first_event.dummy')
 
array = np.ones(100).reshape(10, 10)
wave = hdf54bats.Hdf5Wavefiles('workspace_test', 'first_test')
wave.add_wavefile('first_event.wurb1', 'wurb1_20180101', title='WURB1 20180101', array=array)
wave.add_wavefile('first_event.wurb1', 'dummy', title='DUMMY', array=array)
wave.remove_wavefile('first_event.wurb1.dummy')
 
print('\nChildren: ')
for item_id in wave.get_child_nodes(''):
    print(item_id)
 
print('\nMetadata: ')
events.set_user_metadata('first_event', {'Aaa':'111', 'Bbb':'222'})
wave.set_user_metadata('first_event.wurb1', {'Ccc':'333', 'Ddd':'444'})
wave.set_user_metadata('first_event.wurb1.wurb1_20180101', {'Eee':'555', 'Fff':'666'})

print('\nMetadata first_event: ')
for key, value in events.get_user_metadata('first_event').items():
    print('- key first_event.wurb1: ', key, '   value: ', value)
print('\nMetadata: ')
for key, value in wave.get_user_metadata('first_event.wurb1').items():
    print('- key: ', key, '   value: ', value)
print('\nMetadata first_event.wurb1.wurb1_20180101: ')
for key, value in wave.get_user_metadata('first_event.wurb1.wurb1_20180101').items():
    print('- key: ', key, '   value: ', value)
wave.clear_user_metadata('first_event.wurb1.wurb1_20180101')
print('\nMetadata first_event.wurb1.wurb1_20180101 after clear: ')
for key, value in wave.get_user_metadata('first_event.wurb1.wurb1_20180101').items():
    print('- key: ', key, '   value: ', value)

### Check format.
print('\nFile format: ')
valid_format = samples.check_file()
if valid_format:
    print('- Valid file format.')
else:
    print('- ERROR: Invalid file format.')

### Print content structure. ###
print('\nContent: ')
import tables
f = tables.open_file('workspace_test/first_test.h5', "r")
print(f)

for group in f.walk_groups():
    print(group)
    
for key, group in survey.get_child_groups().items():
    print(key, '   ', group)


f.close()





