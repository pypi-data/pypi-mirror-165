"""
(ZFC) set-theoretic definition of natural numbers.

0 is defined as the empty set ``{}``,
and the rest of the natural numbers
are defined recursively as ``n + 1 = n ∪ {n}``.
"""

from .natural_number import NaturalNumber

__author__ = "Yuanhao 'Nyoeghau' Chen"
__license__ = "MIT"
__email__ = "nyoeghau@nyoeghau.com"

__all__ = ["NaturalNumber"]
