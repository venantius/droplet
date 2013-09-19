#!/usr/bin/env python
# encoding: utf-8

import sys
import unittest

from samplers import L0
from sketches import HyperLogLog

class L0Tests(unittest.TestCase):
    """
    Tests for the L0
    """
    #TODO Various sparsity method checks
    def testSparsity(self):
        #TODO
        pass

    #TODO: Write other test cases

# Sketch tests go here

class HyperLogLogTests(unittest.TestCase):
    """
    Tests for the HyperLogLog sketch
    """
    def testInitializer(self):
        print >> sys.stderr, "Testing HyperLogLog.__init__()..."
        #TODO: ?
        x = HyperLogLog(16)
        x.update(5)
        return 

    def testPrintHLL(self):
        """
        Make sure we're printing all right
        """
        print >> sys.stderr, "Testing HyperLogLog.__repr__()..."
        hll = HyperLogLog(16)
        self.assertEquals(hll.__repr__(), str([0L] * 16))

    def testAddressor(self):
        sample_hll = HyperLogLog(16)
        self.assertTupleEqual((11, 6), sample_hll.address(2954909337))

    def testIndicator(self):
        #TODO
        print >> sys.stderr, "Testing HyperLogLog.indicate()..."
        sample_hll = HyperLogLog(4)
        sample_hll.registers[0] = 6
        sample_hll.registers[1] = 12
        self.assertEquals(sample_hll.indicate(), 0)

    def test(self):
        #TODO: What was I even thinking here?
        pass

def main():
    unittest.main()

if __name__ == "__main__":
    main()

"""
#print "INITIALIZING L0 SAMPLER"
simple_sampler = L0(20, 8)
#print simple_sampler

print "\nTESTING UPDATE FUNCTION\n"
simple_sampler.update(2, 1)
simple_sampler.update(3, 3)
simple_sampler.update(4, 5)
simple_sampler.update(5, 7)
simple_sampler.update(6, 20)
simple_sampler.update(7, 45)
simple_sampler.update(8, 100)
simple_sampler.update(9, 200)
simple_sampler.update(10, 500)

#for _num in range(1,20):
    #    simple_sampler.update(_num, 1)

print simple_sampler

print "\nTESTING RECOVERY FUNCTION:\n"

recovered_weight = simple_sampler.recover()
print recovered_weight
print simple_sampler.recursive_selection()

raw_input('Continue?')
"""

hll_demo = HyperLogLog(2)
print hll_demo
