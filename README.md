py-l0-sampler
=============

Introduction
============

This is the code for an L0-Sampler written in Python. Core algorithm is taken from Cormode & Firmani's (hereafter referred to as "C&F") paper ["On Unifying the Space of L0 Sampling Algorithms"](http://dimacs.rutgers.edu/~graham/pubs/papers/l0samp.pdf) - published at the SIAM Meeting on Algorithm Engineering and Experiments, 2013. The paper (and a good part of this code) is based heavily on prior work published in the L0-sampling space; with that in mind, I have included the following additional papers in the /docs folder for reference:
 - "Counting distinct items over update streams" (Ganguly, 2005)
 - "Sampling in Dynamic Data Streams and Applications" (Frahling, Indyk & Sohler, 2005)
 - "Summarizing and Mining Inverse Distributions on Data Streams via Dynamic Inverse Sampling" (Cormode, Muthukrishnan & Rozenbaum, 2005) 
 - "One sketch for all: Fast algorithms for Compressed Sensing" (Gilbert, Strauss, Tropp & Vershynin, 2007)
 - "Tight Bounds for Lp Samplers, Finding Duplicates in Streams, and Related Problems" (Jowhari, Saglam & Tardos, 2011)

General Notes
-------------
Data structure size is O(s * log<sup>2</sup>(n) * log(s/δ)), though this is generally dominated by the log(n) factor.

Usage
-----

    >> from sampler import L0Sampler
    >> demo\_sampler = L0Sampler(size=20, sparsity=2)
    >> simple\_sampler.update(5, 7)
    >> simple\_sampler.update(6, 20)
    >> simple\_sampler.update(7, 45)
    >> simple\_sampler.update(8, 100)
    >> simple\_sampler.update(9, 200)
    >> simple\_sampler.update(10, 500)
    >> print simple_sampler

    Level 0:

    [(80, False), (200, True), (0, True), (600, False)]
    [(0, True), (505, False), (127, False), (248, False)]

    Level 1:

    [(30, False), (200, True), (0, True), (500, True)]
    [(0, True), (500, True), (27, False), (203, False)]

    Level 2:

    [(30, False), (200, True), (0, True), (0, True)]
    [(0, True), (0, True), (27, False), (203, False)]

    Level 3:

    [(30, False), (0, True), (0, True), (0, True)]
    [(0, True), (0, True), (27, False), (3, True)]

    >> recovered_weight = simple_sampler.recover()
    >> print recovered_weight

    (10, 500)

    >> # Note that at the moment using the sample() method will empty the data
    >> # structure of all items that it can successfully recover
    >> full_sample = simple_sampler.sample()
    >> print full_sample

    [(10, 500), (8, 100), (9, 200), (7, 45)]

"Academic Notes"
================

Choosing k, δ, etc.
-------------------
Figuring out C&F's proposed ideal size (and error) of the Rs data structure (the S-Sparse Recovery Structure) was not readily apparent after on my first couple of read-throughs. 

    we use a two-dimensional array, with log(s/δr) rows and 2s columns

2s is easy as s is our primary parameter, but what to make of δr? In the proof for Lemma 2.1, C&F claim that 
    
    Setting s = 12log(1/δt) we ensure that we can recover at this level j with high 
    probability (and possibly also recover at higher levels j as well).

Solving for the above, we see that δt = 2<sup>-(s/12)</sup>.

We also have δr = δt (though I'm concerned that I've misunderstood this) from Section 2.4, which I think firmly closes the loop. Plugging all of this in guarantees us k >= s/2 as well as gives us a clear idea of what we can expect the error to be.
