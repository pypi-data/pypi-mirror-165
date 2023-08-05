from __future__ import annotations

from numbers import Number
from typing import AbstractSet, Any, Iterable, Iterator, overload


class NaturalNumber(AbstractSet):
    """
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
    """

    _nat_num: int

    def __new__(cls, natural_number: int = 0) -> NaturalNumber:
        if natural_number < 0:
            raise ValueError("Natural number must be non-negative.")
        instance = object.__new__(cls)
        instance._nat_num = natural_number
        return instance

    def __contains__(self, obj: object) -> bool:
        if isinstance(obj, NaturalNumber):
            return self._nat_num > obj._nat_num
        return False

    def __iter__(self) -> Iterator[NaturalNumber]:
        return (NaturalNumber(_nat_num) for _nat_num in range(self._nat_num))

    def __len__(self) -> int:
        return self._nat_num

    @overload
    def __and__(self, other: NaturalNumber) -> NaturalNumber:
        ...

    @overload
    def __and__(self, other: AbstractSet) -> AbstractSet:
        ...

    def __and__(self, other: AbstractSet) -> AbstractSet:
        if isinstance(other, NaturalNumber):
            return NaturalNumber(min(self._nat_num, other._nat_num))
        return self.as_frozenset.__and__(other)

    @overload
    def __rand__(self, other: NaturalNumber) -> NaturalNumber:
        ...

    @overload
    def __rand__(self, other: AbstractSet) -> AbstractSet:
        ...

    def __rand__(self, other: AbstractSet) -> AbstractSet:  # pragma: no cover
        return self.__and__(other)

    @overload
    def __or__(self, other: NaturalNumber) -> NaturalNumber:
        ...

    @overload
    def __or__(self, other: AbstractSet) -> AbstractSet:
        ...

    def __or__(self, other: AbstractSet) -> AbstractSet:
        if isinstance(other, NaturalNumber):
            return NaturalNumber(max(self._nat_num, other._nat_num))
        return self.as_frozenset.__or__(other)

    @overload
    def __ror__(self, other: NaturalNumber) -> NaturalNumber:
        ...

    @overload
    def __ror__(self, other: AbstractSet) -> AbstractSet:
        ...

    def __ror__(self, other: AbstractSet) -> AbstractSet:  # pragma: no cover
        return self.__or__(other)

    @overload
    def __sub__(self, other: NaturalNumber) -> NaturalNumber:
        ...

    @overload
    def __sub__(self, other: AbstractSet) -> AbstractSet:
        ...

    def __sub__(self, other: AbstractSet) -> AbstractSet:
        if isinstance(other, NaturalNumber):
            return NaturalNumber(max(self._nat_num - other._nat_num, 0))
        return self.as_frozenset.__sub__(other)

    @overload
    def __rsub__(self, other: NaturalNumber) -> NaturalNumber:
        ...

    @overload
    def __rsub__(self, other: AbstractSet) -> AbstractSet:
        ...

    def __rsub__(self, other: AbstractSet) -> AbstractSet:
        if isinstance(other, NaturalNumber):  # pragma: no cover
            return NaturalNumber(max(other._nat_num - self._nat_num, 0))
        return other.__sub__(self.as_frozenset)

    def __xor__(self, other: AbstractSet) -> AbstractSet:
        if isinstance(other, NaturalNumber):
            return self.as_frozenset.__xor__(other.as_frozenset)
        return self.as_frozenset.__xor__(other)

    def __rxor__(self, other: AbstractSet) -> AbstractSet:  # pragma: no cover
        return self.__xor__(other)

    def __int__(self) -> int:
        return self._nat_num

    def __index__(self) -> int:
        return int(self)

    def __float__(self) -> float:
        return float(int(self))

    def __bool__(self) -> bool:
        return self._nat_num != 0

    def __pos__(self) -> NaturalNumber:
        return self

    def __abs__(self) -> NaturalNumber:
        return self

    def __add__(self, other: NaturalNumber | int) -> NaturalNumber:
        if isinstance(other, NaturalNumber):
            return NaturalNumber(self._nat_num + other._nat_num)
        if isinstance(other, int):
            return NaturalNumber(self._nat_num + other)
        raise TypeError(
            "unsupported operand type(s) for +: 'NaturalNumber' and '{}'".format(
                type(other)
            )
        )

    def __radd__(self, other: NaturalNumber | int) -> NaturalNumber:  # pragma: no cover
        return self.__add__(other)

    def __repr__(self) -> str:
        return self._nat_num.__repr__()

    def __hash__(self) -> int:
        return self._nat_num

    def __eq__(self, other) -> bool:
        if isinstance(other, NaturalNumber):
            return self._nat_num == other._nat_num
        return False

    def isdisjoint(self, other: Iterable[Any]) -> bool:  # pragma: no cover
        return self.as_frozenset.isdisjoint(other)

    def intersection(
        self, other: Iterable[Any]
    ) -> frozenset[NaturalNumber]:  # pragma: no cover
        return self.as_frozenset.intersection(other)

    def difference(
        self, other: Iterable[Any]
    ) -> frozenset[NaturalNumber]:  # pragma: no cover
        return self.as_frozenset.difference(other)

    def symmetric_difference(
        self, other: Iterable[Any]
    ) -> frozenset[NaturalNumber]:  # pragma: no cover
        return self.as_frozenset.symmetric_difference(other)

    def union(
        self, other: Iterable[Any]
    ) -> frozenset[NaturalNumber]:  # pragma: no cover
        return self.as_frozenset.union(other)

    def issubset(self, other: AbstractSet) -> bool:  # pragma: no cover
        return self.as_frozenset.issubset(other)

    def issuperset(self, other: AbstractSet) -> bool:  # pragma: no cover
        return self.as_frozenset.issuperset(other)

    @property
    def real(self) -> int:  # pragma: no cover
        return self._nat_num.real

    @property
    def imag(self) -> int:  # pragma: no cover
        return self._nat_num.imag

    @property
    def numerator(self) -> int:  # pragma: no cover
        """Integers are their own numerators."""
        return self._nat_num

    @property
    def denominator(self) -> int:  # pragma: no cover
        """Integers have a denominator of 1."""
        return 1

    @property
    def as_frozenset(self) -> frozenset[NaturalNumber]:  # pragma: no cover
        return frozenset(self.__iter__())


Number.register(NaturalNumber)
