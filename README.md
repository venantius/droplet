py-l0-sampler
=============

An L0-Sampler written in Python. Core algorithm is taken from Cormode & Firmani's paper ["On Unifying the Space of L0 Sampling Algorithms"](http://dimacs.rutgers.edu/~graham/pubs/papers/l0samp.pdf) - published at the SIAM Meeting on Algorithm Engineering and Experiments, 2013.

Notes
=====

Choosing k, δ, etc.
-------------------
Figuring out C&F's proposed ideal size (and error) of the Rs data structure (the S-Sparse Recovery Structure) is not readily apparent after a single read-through. 

    we use a two-dimensional array, with log(s/δr) rows and 2s columns

2s is easy as s is our primary paramater, but what to make of δr? In the proof for Lemma 2.1, C&F claim that 
    
    Setting s = 12log(1/δt) we ensure that we can recover at this level j with high 
    probability (and possibly also recover at higher levels j as well).

Solving for the above, we see that δt = 2 ^ -(s/12). 

We also have δr = δt (though I'm a little less sure about this) from Section 2.4, which I think firmly closes the loop. Plugging all of this in, I think, guarantees us k >= s/2 as well as gives us a clear idea of what we can expect the error to be
