Droplet
=======

Introduction
------------
Droplet is a Python library for sampling, sketching and summarizing massive data streams. More information can be found on the [wiki](https://github.com/venantius/droplet/wiki).

Contents
--------
Samplers:
* L<sub>0</sub>-sampler

Sketches:
* Count-min (TODO)
* Top-k (TODO)
* HyperLogLog (TODO)

Summaries:
* TBD

Installation guide
------------------
Pretty simple, really. From the terminal:

    git clone https://github.com/venantius/droplet.git
    cd droplet
    python setup.py install 

Usage
-----
Droplet is designed for use with massive data streams (GB+,TB+, etc.) that may only be read once. 

EXAMPLE GOES HERE

Dependencies
------------
Pypi:
 - mmh3

License
-------
Droplet is licensed under the Apache license. 
