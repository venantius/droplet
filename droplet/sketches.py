#!/usr/bin/env python
# encoding: utf-8

"""
Droplet - Sketches

Sketches for massive data streams.
"""

import sys

from droplet.hash_functions import murmurhash3_32

class CountMin(object):
    #TODO
    pass

class KMin(object):
    #TODO
    pass

class PCSA(object):
    #TODO
    pass

class HyperLogLog(object):
    """
    A naive implementation of the HyperLogLog data structure, as initially 
    described in 2007 by Flajolet, Fusy, et al. in "HyperLogLog: the analysis 
    of a near-optimal cardinality estimation algorithm"

    HLLs are a highly efficient distinct value estimator.

    NOTE: The number of registers should be an integer power of 2.
    """
    class Register(object):
        pass

    def __init__(self, register_count, hash_function = murmurhash3_32):
        if register_count % 2 != 0:
            raise Exception, "ERROR: register count should be an integer" \
                " power of 2"
        self.register_list = [] * int(register_count)
        self.hash_function = hash_function

    def update(self, item):
        """
        Updates the HLL with a new item from the stream
        """
        x = self.hash_function(item)
        print x

