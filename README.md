# Lattice Homology of Seifert Homology Spheres

This repository contains some code for computing the lattice homology and related homology cobordism invariants of Seifert homology spheres.
In particular, it also supports computing the $d$-invariant and maximal monotone subroot of the lattice homology. 
The graded roots are plotted using `networkx` and saved in `.png` files.

There are still a few files that I need to clean up and add documentation to, but hopefully I will have time to get to that soon.
In addition, I implemented a rather "naive" method of calculating the maximal monotone subroot to ensure that I didn't accidentally introduce any errors,
but I will soon implement the faster algorithm.

The main files:
* [`tau_extrema_sequence.py`](https://github.com/willwin4sure/lattice-homology/blob/main/tau_extrema_sequence.py) lays the foundation with code that computes some necessary constants as well as the $\Delta$-function and local extrema of the $\tau$-sequence.
* [`find_d_invariant.py`](https://github.com/willwin4sure/lattice-homology/blob/main/find_d_invariant.py) includes code for computing the $d$-invariant.
* [`graded_roots.py`](https://github.com/willwin4sure/lattice-homology/blob/main/graded_roots.py) includes code for computing and drawing the lattice homology as well as maximal monotone subroot. I will soon implement a faster method of computing the maximal monotone subroot.
* [`generate_grid.py`](https://github.com/willwin4sure/lattice-homology/blob/main/generate_grid.py) includes code for automatically generating the pictorial grid representation into an Excel spreadsheet.

## About

This code was initially written as part of a MIT PRIMES project mentored by Dr. Irving Dai of Stanford University. 
I worked with coauthors Karthik Seetharaman and Isaac Zhu on the project, and they contributed to some of the code found in this repository.
Our paper can be found on arXiv here: https://arxiv.org/abs/2110.13405.

Finally, I expanded on the code as part of my research project in the CSC 600 class at Phillips Academy Andover, 
where I managed to prove more results about the periodicity of the maximal monotone subroot.

## Contribute

Feel free to contribute by simply forking the repository and submitting a pull request. 