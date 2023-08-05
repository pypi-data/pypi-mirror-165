from numbers import Number
from typing import AbstractSet

from zfc import NaturalNumber

from .utils import BaseTestCase


class TestZFC(BaseTestCase):
    def test_zfc(self):
        with self.assertRaises(ValueError):
            NaturalNumber(-1)

        zero = NaturalNumber(0)
        one = NaturalNumber(1)
        one2 = NaturalNumber(1)
        two = NaturalNumber(2)

        self.assertNotEqualAndHashNotEqual(zero, one)
        self.assertEqualAndHashEqual(zero, zero)
        self.assertEqualAndHashEqual(one, one2)

        self.assertGreater(one, zero)

        self.assertIn(zero, one)
        self.assertNotIn(frozenset(zero), one)

        self.assertEqualAndHashEqual(two & one, one)
        self.assertSetEqual(two & set(one), one.as_frozenset)

        self.assertEqualAndHashEqual(one | two, two)
        self.assertEqualAndHashEqual(one | set(two), two.as_frozenset)

        self.assertEqualAndHashEqual(two - one, one)
        self.assertEqualAndHashEqual(one - two, zero)
        self.assertSetEqual(two - set(one), {one})

        self.assertSetEqual(set(two) - one, {one})

        self.assertSetEqual(one ^ one, set())
        self.assertSetEqual(one ^ set(two), {one})

        self.assertEqualAndHashEqual(int(zero), 0)

        self.assertEqualAndHashEqual(two.__int__(), two.__index__())

        self.assertEqualAndHashEqual(float(two), 2.0)

        self.assertTrue(one)
        self.assertFalse(zero)

        self.assertEqualAndHashEqual(one, +one)

        self.assertEqualAndHashEqual(one, abs(one))

        self.assertEqualAndHashEqual(one, zero + 1)
        self.assertEqualAndHashEqual(two, one + one)
        with self.assertRaises(TypeError):
            one + set()

        self.assertEqualAndHashEqual(repr(1), repr(one))

        self.assertNotEqual(zero, frozenset())

        self.assertTrue(issubclass(NaturalNumber, Number))
        self.assertTrue(issubclass(NaturalNumber, AbstractSet))
        self.assertTrue(isinstance(one, (Number, AbstractSet)))
