#!/usr/bin/env python
# encoding: utf-8

"""
This is a prototype for an L0 sampler. 

Creation date: 2013-03-27
"""

import math
import mmh3
from operator import attrgetter
import random
import sys

class OneSparseRecoveryEstimator():
    """
    A straightforward implementation of a one-sparse recovery estimator.
    
    Includes sparsity checks at varying levels of complexity
    """
    def __init__(self):
        self.phi = 0
        self.iota = 0
        self.tau = 0

    def __eq__(self, other):
        if (self.phi == other.phi and \
            self.iota == other.iota and \
            self.tau == other.tau):
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.phi, self.iota, self.tau))

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
        #TODO
        pass

class SSparseRecoveryEstimator(object):
    """
    An s-sparse recovery estimator comprised of an array of 1-sparse estimators
    """
    def __init__(self, ncols, nrows):
        self.ncols = ncols
        self.nrows = nrows
        self.array = [[OneSparseRecoveryEstimator() for _s 
            in range(self.ncols)] for _ in range(self.nrows)]

    def __repr__(self):
        return '\n'.join([str(x) for x in self.array])

    def is_s_sparse(self):
        """
        Check to see if this level is s-sparse
        """
        sparsity = 0
        size = self.ncols * self.nrows
        for row in self.array:
            sparsity += [item.phi for item in row].count(0)
        if sparsity >= (self.ncols / 2) and sparsity != size:
            return True
        else:
            return False

    def update(self, i, value):
        """
        Update the s-sparse recovery estimator at each hash function
        """
        for row in range(self.nrows):
            col = mmh3.hash(str(i), seed=row) % self.ncols
            self.array[row][col].update(i, value)

    def recover(self, i):
        """
        Attempt to recover a nonzero vector from this level
        """
        a_prime = set()
        for row in range(self.nrows):
            for col in range(self.ncols):
                if self.array[row][col].phi != 0 and \
                    self.array[row][col].is_one_sparse_ganguly():
                    a_prime.add(self.array[row][col])
        return a_prime

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
        self.size = size
        self.sparsity = sparsity
        self.k = k
        levels = int(round(math.log(size, 2)))
        self.levels = [SSparseRecoveryEstimator(self.sparsity * 2, k) 
                for _ in range(levels)]

    def __repr__(self):
        return_str = []
        for depth, level in enumerate(self.levels):
            return_str.append("Level %s:" % depth)
            return_str.append(str(level))

        return '\n\n'.join(return_str)

    def recover(self, i=None):
        """
        Attempt to recover a nonzero vector from one of the L0 Sampler's levels.
        """
        if not i:
            i = random.randint(0, self.size-1)
        for j, level in enumerate(self.levels):
            if level.is_s_sparse():
                #print >> sys.stderr, "Identified level %s as s-sparse; recovering..." % j
                vector = level.recover(i)
                if vector:
                    break
                else: 
                    #print >> sys.stderr, "Failed to recover at level %s, trying level %s" % (j, j+1)
                    continue
        #print "\n\n" + str(self) + "\n\n"
        if vector:
            selection = self.select(vector)
            return selection
        else:
            return None

    def sample(self):
        sample = []
        while True:
            selection = self.recover()
            if not selection:
                break
            sample.append(selection)
            self.update(selection[0], -selection[1])
            #print "RECOVERED: %s" % str(selection)
        return sample

    def select(self, vector):
        #print "A'(j): %s" % vector
        indexes = sorted(vector, key=lambda x: mmh3.hash(str(x.iota / x.phi)))
        item = indexes[0]
        i = item.iota / item.phi
        return (i, item.phi)

    def update(self, i, value):
        """
        Update the L0 sampler
        """
        if not (i > 0 and i <= self.size):
            raise Exception, "Update value %s outside size %s" % (i, self.size)
        for j, level in enumerate(self.levels):
            if self.size * (2 ** -(j + 1)) >= \
                (mmh3.hash(str(i)) % self.size) + 1:
                level.update(i, value)
