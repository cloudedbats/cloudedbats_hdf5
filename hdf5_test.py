#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2018 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

# Library: hdf54bats, HDF5 for bats.
# Test during development. 

import numpy as np
import hdf54bats

ws = hdf54bats.Hdf5Workspace('workspace_test')
ws.delete_hdf5('first_test')
ws.create_hdf5('first_test') # Not mandatory, will be created later.


survey = hdf54bats.Hdf5Survey('workspace_test', 'first_test')
survey.add_survey('', 'first_survey')
survey.add_survey('', 'dummy', 'DUMMY')
survey.remove_survey('dummy')

event = hdf54bats.Hdf5Event('workspace_test', 'first_test')
event.add_event('first_survey', 'first_event')
event.add_event('first_survey', 'dummy', 'DUMMY')
event.remove_event('first_survey.dummy')
 
detector = hdf54bats.Hdf5Detector('workspace_test', 'first_test')
detector.add_detector('first_survey.first_event', 'wurb1')
detector.add_detector('first_survey.first_event', 'dummy', 'DUMMY')
detector.remove_detector('first_survey.first_event.dummy')
 
array = np.ones(100).reshape(10, 10)
wave = hdf54bats.Hdf5Wavefile('workspace_test', 'first_test')
wave.add_wavefile('first_survey.first_event.wurb1', 'wurb1_20180101', 'WURB1 20180101', array)
wave.add_wavefile('first_survey.first_event.wurb1', 'dummy', 'DUMMY', array)
wave.remove_wavefile('first_survey.first_event.wurb1.dummy')
 
print('\nChildren: ')
wave.get_children('first_survey')
 
print('\nMetadata: ')
event.set_user_metadata('first_survey.first_event', {'Aaa':'111', 'Bbb':'222'})
wave.set_user_metadata('first_survey.first_event.wurb1', {'Ccc':'333', 'Ddd':'444'})
wave.set_user_metadata('first_survey.first_event.wurb1.wurb1_20180101', {'Eee':'555', 'Fff':'666'})

print('\nMetadata first_survey.first_event: ')
for key, value in event.get_user_metadata('first_survey.first_event').items():
    print('- key first_survey.first_event.wurb1: ', key, '   value: ', value)
print('\nMetadata: ')
for key, value in wave.get_user_metadata('first_survey.first_event.wurb1').items():
    print('- key: ', key, '   value: ', value)
print('\nMetadata first_survey.first_event.wurb1.wurb1_20180101: ')
for key, value in wave.get_user_metadata('first_survey.first_event.wurb1.wurb1_20180101').items():
    print('- key: ', key, '   value: ', value)
wave.clear_user_metadata('first_survey.first_event.wurb1.wurb1_20180101')
print('\nMetadata first_survey.first_event.wurb1.wurb1_20180101 after clear: ')
for key, value in wave.get_user_metadata('first_survey.first_event.wurb1.wurb1_20180101').items():
    print('- key: ', key, '   value: ', value)

### Check format.
print('\nFile format: ')
valid_format = detector.check_file()
if valid_format:
    print('- Valid file format.')
else:
    print('- ERROR: Invalid file format.')

### Print content structure. ###
print('\nContent: ')
import tables
f = tables.open_file('workspace_test/first_test.h5', "r")
print(f)
f.close()





