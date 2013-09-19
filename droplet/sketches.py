#!/usr/bin/env python
# encoding: utf-8

"""
Droplet - Sketches

Sketches for massive data streams.
"""

import ctypes
import math
import sys

from array import array

from droplet.hash_functions import murmurhash3_32

class HyperLogLog(object):
    """
    A naive implementation of the HyperLogLog data structure, as initially 
    described in 2007 by Flajolet, Fusy, et al. in "HyperLogLog: the analysis 
    of a near-optimal cardinality estimation algorithm"

    Registers are kept as an array of 32-bit unsigned integers. 
    #TODO: expand with functionality for 64-bit integers

    HLLs are a highly efficient distinct value estimator.

    NOTE: The number of registers should be an integer power of 2.
    """
    def __init__(self, register_count, hash_function = murmurhash3_32):
        if register_count % 2 != 0:
            raise Exception, "ERROR: register count should be an integer" \
                " power of 2"
        self.register_count = int(register_count)
        self.address_length = int(math.sqrt(self.register_count))
        self.registers = array('I', [0] * register_count)
        self.hash_function = hash_function

    def __repr__(self):
        return str([register for register in self.registers])

    @staticmethod
    def uint32(integer):
        """
        Convert a potentially signed integer to an unsigned int
        """
        return ctypes.c_uint32(integer).value

    def update(self, item):
        """
        Updates the HLL with a new item from the stream
        """
        hash_output = self.hash_function(item)
        register_index, value = self.address(hash_output)
        self.registers[register_index] = max(self.registers[register_index], 
                value)
    
    def address(self, integer):
        """
        Returns the integer position of the left-most 1
        """
        hashed_value = bin(self.uint32(integer)) # in case we get a signed int
        if len(hashed_value) < 34:
            hashed_value = '0b' + '0' * (34 - len(hashed_value)) + \
                hashed_value[2:]
        elif len(hashed_value) == 34:
            pass
        else:
            raise Exception
        register_index, value = hashed_value[2:2 + self.address_length], \
            hashed_value[2 + self.address_length:]
        # Evaluate the binary address into an integer
        register_index = eval('0b' + register_index)
        value = value.find('1')
        return register_index, value

    def indicate(self):
        indicator = 0
        for x in range(len(self.registers)):
            # Look up how to most efficiently sum numbers in python
            indicator += 2 ** -self.registers[x]
            print 2 ** -self.registers[x]
        print indicator
        return indicator

class CountMin(object):
    #TODO
    pass

class KMin(object):
    #TODO
    pass

class PCSA(object):
    #TODO
    pass
