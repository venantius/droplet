#!/usr/bin/env python
# encoding: utf-8

"""
Samplers.py

Data structures for the dynamic sampling of massive streams of data:
    - L0-Sampler
    - Distinct Sampler
"""

import math
import random

from droplet.hash_functions import murmurhash3_32

#TODO: nest the sub-classes under the master class
#TODO: Write test cases for the L0 sampler
#TODO: Alter the way it hashes so that it hashes to one row in a level rather than all rows in a level (like HLL rather than your naive implementation)

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
        A slightly more advanced check to see if P1 is one-sparse.

        In cases where updates are assumed to be non-negative, this is 
        sufficient. In cases requiring negative updates, use 
        is_one_sparse_prime() instead.
        """
        if self.phi * self.tau == (self.iota ** 2):
            return True
        else: 
            return False

    def is_one_sparse_prime(self, index):
        """
        An advanced check to see if P1 is one-sparse (using large primes).

        May register a false negative; see the wiki for more details.
        """
        #TODO
        pass

class SSparseRecoveryEstimator(object):
    """
    An s-sparse recovery estimator comprised of an array of 1-sparse estimators
    """
    def __init__(self, ncols, nrows, hash_function):
        self.ncols = ncols
        self.nrows = nrows
        self.array = [[OneSparseRecoveryEstimator() for _s 
            in range(self.ncols)] for _ in range(self.nrows)]
        
        self.hash_function = hash_function

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
            col = self.hash_function(str(i), seed=row) % self.ncols
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

class L0(object):
    """
    A naive implementation of an L0-Sampling data structure, as described in 
    Cormode and Firmani's 2013 paper, "On Unifying the Space of L0-Sampling 
    Algorithms"

    N refers to the size of the input space (e.g. an unsigned 64-bit int in the
    case of most cookie ID spaces)

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
    def __init__(self, size, sparsity, k=None, hash_function = murmurhash3_32):
        if not k:
            delta = 2 ** (-sparsity/ 12)
            k = int(round(math.log(sparsity/delta, 2)))
        self.size = size
        self.sparsity = sparsity
        self.k = k
        levels = int(round(math.log(size, 2)))
        self.levels = [SSparseRecoveryEstimator(self.sparsity * 2, k, 
            hash_function) for _ in range(levels)]
        self.hash_function = murmurhash3_32

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
        vector = None
        for level in self.levels:
            if level.is_s_sparse():
                vector = level.recover(i)
                if vector:
                    break
                else: 
                    continue
        if vector:
            return self.select(vector)
        else:
            return None

    def recursive_selection(self):
        """
        Attempts to select (and delete) an item from the data structure until
        either the data structure is empty or no more items can be recovered.
        """
        sample = []
        while True:
            selection = self.recover()
            if not selection:
                break
            sample.append(selection)
            self.update(selection[0], -selection[1])
        return sample

    def select(self, vector):
        """
        Given a vector of recovered items, grabs the one with the lowest hash
        value.
        """
        indexes = sorted(vector, key=lambda x: 
                self.hash_function((str(x.iota / x.phi))))
        item = indexes[0]
        i = item.iota / item.phi
        return (i, item.phi)

    def update(self, i, value):
        """
        Update the L0 sampler. This process generally aligns with the 'sample'
        step as described in section 2 of the paper.
        """
        if not (i > 0 and i <= self.size):
            raise Exception, "Update value %s outside size %s" % (i, self.size)
        for j, level in enumerate(self.levels):
            if self.size * (2 ** -(j + 1)) >= \
                (self.hash_function(str(i)) % self.size) + 1:
                level.update(i, value)
