#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2018-2019 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import string

def str_to_ascii(text):
    """
        Converts group titles to valid group names. Mainly ascii.
    """
    new_text = []
    for c in text.lower().replace(' ', '_'):
        if c in string.ascii_lowercase:
            new_text.append(c)
        elif c in string.digits:
            new_text.append(c)
        elif c in string.punctuation:
            new_text.append('_')
        else:
            if c == 'å': new_text.append('a')
            elif c == 'ä': new_text.append('a')
            elif c == 'ö': new_text.append('o')
            else: new_text.append('_')
    
    return ''.join(new_text)

