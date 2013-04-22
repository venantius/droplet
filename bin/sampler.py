#!/usr/bin/env python
# encoding: utf-8

"""
This is a prototype for an L0 sampler. 

Creation date: 2013-03-27
"""

import math
import mmh3
import random

class OneSparseRecoveryEstimator():
    """
    A straightforward implementation of a one-sparse recovery estimator.
    
    Includes sparsity checks at varying levels of complexity
    """
    def __init__(self):
        self.phi = 0
        self.iota = 0
        self.tau = 0

    def __repr__(self):
        return str((self.phi, self.is_one_sparse_ganguly()))

    def update(self, index, weight):
        """
        Update the recovery estimators
        """
        self.phi += weight
        self.iota += weight * index
        self.tau += weight * (index ** 2)

    def is_one_sparse_simple(self, index):
        """
        The simplest possible check to verify if P1 is indeed one-sparse
        """
        if self.iota / self.phi == index:
            return True
        else:
            return False

    def is_one_sparse_ganguly(self):
        """
        Slightly more advanced check to see if P1 is one-sparse.

        Because AK's frequency updates are assumed to be non-negative (and
        always equal to 1) this is sufficient. If we expected negative updates,
        however, we would need to use F&C's prime-based one-sparse checker
        """
        if self.phi * self.tau == (self.iota ** 2):
            return True
        else: 
            return False

    def is_one_sparse_prime(self, index):
        """
        Advanced check to see if P1 is one-sparse (using large primes)
        """
        pass

class SSparseRecoveryEstimator(object):
    """
    An s-sparse recovery estimator comprised of an array of 1-sparse estimators
    """
    def __init__(self, sparsity, k):
        self.sparsity = sparsity
        self.k = k
        self.array = [[OneSparseRecoveryEstimator() for _s 
            in range(self.sparsity)] for _ in range(k)]

    def __repr__(self):
        return '\n'.join([str(x) for x in self.array])

    def update(self, i, value):
        """
        Update the s-sparse recovery estimator at each hash function
        """
        for row in range(self.k):
            col = mmh3.hash(str(i), seed=row) % self.sparsity
            self.array[row][col].update(i, value)

    def recover(self, i):
        """
        Attempt to recover a nonzero vector from this level
        """
        #TODO

class L0Sampler(object):
    """
    A naive implementation of Cormode and Firmani's L0-Sampling data structure

    N refers to the size of the input space (e.g. an unsigned 64-bit int in the
    case of the ak_user_id)

    k refers to the number of hash functions used in the s-sparse recovery data
    structure.

    s refers to the sparsity of the s-sparse recovery data structure.
    
    In theory, one generally should hold k >= s/2, but in practice C&F 
    note that "it suffices to use small values of k, for instance k=7, to 
    ensure that the failure rate holds steady, independent of the number of 
    reptitions made." Additional notes on this can be found in the 
    accompanying README.

    Also of note: "When time is important, using s<=12 and k<=6 ensures fast 
    computation. On the other hand, by selecting bigger values for both s and 
    k, the process becomes slower than the FIS variant."
    """
    def __init__(self, size, sparsity, k=None):
        if not k:
            delta = 2 ** (-sparsity/ 12)
            k = int(round(math.log(sparsity/delta, 2)))
        #TODO: Set k >= s/2; or log(s/delta)?
        # Need to solve for the above to figure out what k should be set as in the context of s; delta is set by s and k can be set by s and delta, so...
        self.size = size
        self.sparsity = 2 * sparsity
        self.k = k
        levels = int(round(math.log(size, 2)))
        self.levels = [SSparseRecoveryEstimator(self.sparsity, k) 
                for _ in range(levels)]

    def __repr__(self):
        return_str = []
        for depth, level in enumerate(self.levels):
            return_str.append("Level %s:" % depth)
            return_str.append(str(level))

        return '\n\n'.join(return_str)

    def update(self, i, value):
        """
        Update the L0 sampler
        """
        if not (i > 0 and i <= self.size):
            raise Exception, "Update value %s outside of size %s" % (i, self.size)
        for j, level in enumerate(self.levels):
            #print "hash modulo: %s" %  (mmh3.hash(str(i)) % self.size + 1)
            #print "size 2^-j: %s" % (self.size * (2 ** -(j + 1)))
            if self.size * (2 ** -(j + 1)) >= \
                (mmh3.hash(str(i)) % self.size) + 1:
                level.update(i, value)

    def recover(self, i=None):
        """
        Attempt to recover a nonzero vector from one of the L0 Sampler's levels.
        """
        if not i:
            i = random.randint(0, self.size-1)
        for j, level in enumerate(self.levels):
            vector = level.recover(i)
            if vector:
                break
        return vector

#heyo = L0Sampler(2**64, 3)
#print len(heyo.levels)

#print "INITIALIZING L0 SAMPLER"
simple_sampler = L0Sampler(20, 3)
#print simple_sampler

print "\nTESTING UPDATE FUNCTION\n"
simple_sampler.update(2, 1)
simple_sampler.update(3, 3)
simple_sampler.update(4, 5)
simple_sampler.update(5, 7)
#simple_sampler.update(6, 20)
#simple_sampler.update(7, 45)
#simple_sampler.update(8, 100)
#simple_sampler.update(9, 200)
#simple_sampler.update(10, 500)

simple_sampler.recover(10)
print simple_sampler

