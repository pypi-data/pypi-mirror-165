# Pure zero-dependency JSON-RPC 2.0 implementation.
# Copyright © 2022 Andrew Malchuk. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import OrderedDict
from collections.abc import Callable, Hashable, Iterable, Iterator, MutableMapping
from itertools import filterfalse, tee
from typing import Any, Final, Literal, TypeVar, final, overload

from ._typing import SupportsGetItemAndKeys

__all__: Final[list[str]] = [
    "Dict",
    "make_hashable",
    "partition",
    "Undefined",
    "UndefinedType"
]

_K = TypeVar("_K")
_T = TypeVar("_T")
_Self = TypeVar("_Self")


class Dict(MutableMapping[_K, _T]):
    __slots__: list[str] = ["_dict"]

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, /, **kwargs: _T) -> None: ...

    @overload
    def __init__(self, mapping: SupportsGetItemAndKeys[_K, _T], /, **kwargs: _T) -> None: ...

    @overload
    def __init__(self, iterable: Iterable[tuple[_K, _T]], /, **kwargs: _T) -> None: ...

    @final
    def __init__(self, /, *args: Any, **kwargs: Any) -> None:
        self._dict: Final[OrderedDict[_K, _T]] = OrderedDict(*args, **kwargs)

    def __repr__(self) -> str:
        return repr(self._dict)

    def __eq__(self, obj: Any, /) -> bool:
        return isinstance(obj, self.__class__) and self._dict == obj._dict

    def __getitem__(self, key: _K, /) -> _T:
        return self._dict[key]

    def __setitem__(self, key: _K, value: _T, /) -> None:
        self._dict[key] = value
        self._dict.move_to_end(key)

    def __delitem__(self, key: _K, /) -> None:
        del self._dict[key]

    def __len__(self) -> int:
        return len(self._dict)

    def __iter__(self) -> Iterator[_K]:
        return iter(self._dict)

    def __contains__(self, obj: Any, /) -> bool:
        return obj in self._dict

    def __or__(self: type[_Self], mapping: MutableMapping[_K, _T], /) -> _Self:
        if not isinstance(mapping, MutableMapping):
            return NotImplemented

        return self.__class__(self._dict | mapping)

    def __ror__(self: type[_Self], mapping: MutableMapping[_K, _T], /) -> _Self:
        if not isinstance(mapping, MutableMapping):
            return NotImplemented

        return self.__class__(mapping | self._dict)

    def __ior__(self: type[_Self], mapping: MutableMapping[_K, _T], /) -> _Self:
        if not isinstance(mapping, MutableMapping):
            return NotImplemented

        self._dict |= mapping
        return self


def make_hashable(obj: Any, /) -> Hashable:
    if isinstance(obj, MutableMapping):
        return tuple((key, make_hashable(value)) for key, value in sorted(obj.items()))

    # Try hash to avoid converting a hashable iterable (e.g. string, frozenset)
    # to a tuple:
    try:
        hash(obj)
    except TypeError:
        if isinstance(obj, Iterable):
            return tuple(map(make_hashable, obj))
        # Non-hashable, non-iterable:
        raise

    return obj


def partition(predicate: Callable[[_T], bool] | None, iterable: Iterable[_T], /) -> Iterator[_T]:
    """
    Use a predicate to partition entries into true entries and false entries.
    """
    left, right = tee(iterable)
    yield from filter(predicate, left)
    yield from filterfalse(predicate, right)


class UndefinedType:
    __slots__: tuple[str, ...] = ()

    def __repr__(self) -> Literal["Undefined"]:
        return "Undefined"

    def __hash__(self) -> Literal[0xDEADBEEF]:
        return 0xDEADBEEF

    def __eq__(self, obj: Any, /) -> bool:
        return isinstance(obj, self.__class__)

    def __bool__(self) -> Literal[False]:
        return False


Undefined: Final[UndefinedType] = UndefinedType()
