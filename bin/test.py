#!/usr/bin/env python
# encoding: utf-8

from sampler import L0Sampler

#print "INITIALIZING L0 SAMPLER"
simple_sampler = L0Sampler(20, 2)
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

for _num in range(1,20):
    simple_sampler.update(_num, 1)

print simple_sampler

print "\nTESTING RECOVERY FUNCTION:\n"

print simple_sampler.sample()

