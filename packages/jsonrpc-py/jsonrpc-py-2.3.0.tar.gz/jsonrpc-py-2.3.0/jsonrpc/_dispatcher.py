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

from abc import ABCMeta, abstractmethod
from collections.abc import Callable
from functools import partial
from inspect import Signature, isfunction
from typing import Any, Final, TypeVar

from ._errors import Error, ErrorEnum
from ._utilities import Dict

__all__: Final[list[str]] = ["Dispatcher"]

_F = TypeVar("_F", bound=Callable)


class BaseDispatcher(Dict[str, Callable], metaclass=ABCMeta):
    __slots__: tuple[str, ...] = ()

    def __hash__(self) -> int:
        return hash(objects := frozenset(self.items())) ^ len(objects)

    @abstractmethod
    def register(self, user_function: _F | None = None, *, function_name: str | None = None) -> _F | Callable[[_F], _F]:
        raise NotImplementedError

    @abstractmethod
    def dispatch(self, function_name: str, /, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


class Dispatcher(BaseDispatcher):
    """
    The :py:class:`collections.abc.MutableMapping` subclass representing the storage of user-defined functions.
    """
    __slots__: tuple[str, ...] = ()

    def __repr__(self) -> str:
        return f"<{self.__class__.__qualname__}()>"

    def register(self, user_function: _F | None = None, *, function_name: str | None = None) -> _F | Callable[[_F], _F]:
        """
        Add the user-defined function to the dispatcher.
        Be sure that your function is passing by the :py:func:`inspect.isfunction` method.

        Example usage::

            >>> dispatcher = Dispatcher()
            >>> dispatcher.register(lambda a, b: a + b)
            <function <lambda> at 0x\u2026>

        Probably, you want use it as a decorator? Let's go::

            >>> @dispatcher.register
            ... def add(a: float, b: float) -> float:
            ...     return a + b

        Do you want to use the different function's name? No problem::

            >>> @dispatcher.register(function_name="sum")
            ... def _(a: float, b: float) -> float:
            ...     return a + b

        :param user_function: The :py:data:`types.FunctionType` object representing the user-defined function.
        :param function_name: An optional function's name. If it is omitted, attribute ``__name__`` will be used instead.
        :raises RuntimeError: If the ``user_function`` isn't passed by the :py:func:`inspect.isfunction` method,
            or function with the provided name is already defined in the :class:`jsonrpc.Dispatcher` class.
        :returns: The unmodified ``user_function`` object, passed in the parameters.
        """
        if user_function is None:
            return partial(self.register, function_name=function_name)

        if not isfunction(user_function):
            raise RuntimeError(f"{type(user_function).__name__!r} isn't a user-defined function")

        if (function_name := user_function.__name__ if function_name is None else function_name) in self:
            raise RuntimeError(f"{function_name!r} is already defined in {self[function_name].__module__!r}")

        self[function_name] = user_function
        return user_function

    def dispatch(self, function_name: str, /, *args: Any, **kwargs: Any) -> Any:
        """
        Invoke the user-defined function by passed in parameters function's name.

        Example usage::

            >>> dispatcher = Dispatcher()
            >>> dispatcher.dispatch("sum", a=12, b=34)
            46

        :param function_name: The user-defined function's name.
        :param args: Positional arguments for the provided function.
        :param kwargs: Keyword arguments for the provided function.
        :raises jsonrpc.Error: If the function doesn't exists in the :class:`jsonrpc.Dispatcher` class,
            passed invalid parameters or unexpected internal error has raised. See also :class:`jsonrpc.ErrorEnum`.
        :returns: Result of execution the user-defined function.
        """
        try:
            user_function: Final[Callable] = self[function_name]
        except KeyError as exc:
            raise Error(code=ErrorEnum.METHOD_NOT_FOUND, message=f"Function {function_name!r} isn't found") from exc

        try:
            Signature.from_callable(user_function).bind(*args, **kwargs)
        except TypeError as exc:
            raise Error(code=ErrorEnum.INVALID_PARAMETERS, message=f"Invalid parameters: {exc!s}") from exc

        try:
            return user_function(*args, **kwargs)
        except Error:
            raise
        except Exception as exc:
            raise Error(code=ErrorEnum.INTERNAL_ERROR, message=f"Unexpected internal error: {exc!s}") from exc
