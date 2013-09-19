#!/usr/bin/env python
# encoding: utf-8

"""
A set of hash functions known to have good uniformity properties
"""

import mmh3 

def murmurhash3_32(item, seed = 0):
    """
    Murmurhash 3 for 32-bit integers
    """
    if type(item) is not str: 
        item = str(item)
    if type(seed) is not int:
        seed = int(seed)
    return mmh3.hash(item, seed = seed)

def murmurhash3_64(item, seed = 0):
    """
    Murmurhash 3 for 64-bit integers (returns the first of a tuple of two)
    """
    if type(item) is not str: 
        item = str(item)
    if type(seed) is not int:
        seed = int(seed)
    return mmh3.hash64(item, seed = seed)
