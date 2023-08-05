# ZFC: set-theoretic definition of natural numbers in Python

<p align="center">
    <a href="https://github.com/edward-martyr/ZFC/actions?query=workflow%3Abuild"><img src="https://github.com/edward-martyr/ZFC/workflows/build/badge.svg?branch=master" alt="build"></a>
    <a href="https://github.com/edward-martyr/ZFC/actions?query=workflow%3Alint"><img src="https://github.com/edward-martyr/ZFC/workflows/lint/badge.svg?branch=master" alt="lint"></a>
    <a href="https://codecov.io/gh/edward-martyr/ZFC"><img src="https://img.shields.io/codecov/c/github/edward-martyr/ZFC?token=WZSLMLQV72" alt="coverage"></a>
</p>
<p align="center">
    <a href="https://pypi.org/project/pyZFC/"><img src="https://img.shields.io/pypi/v/pyZFC.svg" alt="pypi"></a>
    <a href="https://img.shields.io/pypi/pyversions/pyZFC"><img src="https://img.shields.io/pypi/pyversions/pyZFC" alt="support-version"></a>
    <a href="https://github.com/edward-martyr/ZFC/blob/master/LICENSE.txt"><img src="https://img.shields.io/github/license/edward-martyr/ZFC" alt="license"></a>
    <a href="https://github.com/edward-martyr/ZFC/commits/master"><img src="https://img.shields.io/github/last-commit/edward-martyr/ZFC" alt="commit"></a>
</p>

## Installation

```shell
pip install pyZFC
```

## Introduction and examples

``NaturalNumber`` is the class of natural numbers defined
as von Neumann ordinals in the ZFC set theory.

0 is defined as the empty set ``{}``,
and the rest of the natural numbers
are defined recursively as ``n + 1 = n ∪ {n}``,
i.e.,

```math
0 = {},
1 = {0},
2 = {0, 1},
3 = {0, 1, 2},
...
```

Following the definition, you can do all kinds of
set operations on natural numbers, e.g., checking
whether a ``NaturalNumber`` contains another.

```Python console
>>> from zfc import NaturalNumber

>>> NaturalNumber(1) in NaturalNumber(2)
True

>>> NaturalNumber(1) & NaturalNumber(2)
1  # the intersection of 1={0} and 2={0,1} is {0}, which is exactly 1.
```
