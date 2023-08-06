# enstat

[![CI](https://github.com/tdegeus/enstat/workflows/CI/badge.svg)](https://github.com/tdegeus/enstat/actions)
[![Documentation Status](https://readthedocs.org/projects/enstat/badge/?version=latest)](https://enstat.readthedocs.io)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/enstat.svg)](https://anaconda.org/conda-forge/enstat)
[![PyPi release](https://img.shields.io/pypi/v/enstat.svg)](https://pypi.org/project/enstat/)

Documentation: [enstat.readthedocs.io](https://enstat.readthedocs.io)

# Overview

*enstat* is a library to facilitate the computation of ensemble averages
(and their standard deviation and variance).
The key feature is that a class stored the sum of the first and second statistical moments
and the number of samples,
such that adding a sample can be done trivially, while giving access to the mean etc.
at all times.

# Disclaimer

This library is free to use under the
[MIT license](https://github.com/tdegeus/enstat/blob/master/LICENSE).
Any additions are very much appreciated, in terms of suggested functionality, code,
documentation, testimonials, word-of-mouth advertisement, etc.
Bug reports or feature requests can be filed on
[GitHub](https://github.com/tdegeus/enstat).
As always, the code comes with no guarantee.
None of the developers can be held responsible for possible mistakes.

Download:
[.zip file](https://github.com/tdegeus/enstat/zipball/master) |
[.tar.gz file](https://github.com/tdegeus/enstat/tarball/master).

(c - [MIT](https://github.com/tdegeus/enstat/blob/master/LICENSE))
T.W.J. de Geus (Tom) | tom@geus.me | www.geus.me |
[github.com/tdegeus/enstat](https://github.com/tdegeus/enstat)

# Installation

## Using conda

```bash
conda install -c conda-forge enstat
```

## Using PyPi

```bash
pip install enstat
```

# Change-log

## v0.5.0

*   [BREAKING CHANGE] Changing `shape`, `size`, `dtype`, `first`, `second`, `norm` to properties rather than functions (now call without `()`)
*   Adding `add_point` to array classes
*   [tests] Using unittest discover
*   [docs] Using furo theme. Minor updates.

## v0.4.1

*   Enforcing shape to be a tuple (like in NumPy) (#14)

## v0.4.0

*   Simplifying namespace. Using opportunity to simplify class names
*   Avoiding zero division warning
*   Adding test with defaultdict

## v0.3.1

*   Return NaN when there is no data (before zero was returned)
*   (style) Fixing pre-commit
*   (style) Renaming "test" -> "tests"
*   (style) Applying pre-commit

## v0.3.0

*   Adding mask option to `enstat.static.StaticNd`.

## v0.2.0

*   Adding size and shape methods.
*   Various generalisations.
