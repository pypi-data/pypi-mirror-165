# -*- coding: utf-8 -*-

"""This Module provides an error handling utility class with
`try except` wrapper.

Example:
    from trycatch import Try
"""

__version__ = "1.0.3"

from typing import Any, Awaitable, Callable, Tuple, Type, TypeVar, Union

T = TypeVar("T")


class Try:
    """Class to wrap a function or method in preparation
    to catch exceptions.
    """

    def __init__(
        self,
        func: Callable[..., Union[T, Awaitable[T]]],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Instantiates a `Try` instance.

        Args:
            func (Callable): The function or method in context,
            could be either sync or async.
            *args: Variable length argument list for `func`.
            **kwargs: Arbitrary keyword arguments for `func`.

        Raises:
            TypeError: If `func` argument is not a `Callable`.
        """

        if not callable(func):
            raise TypeError("`func` argument must be a Callable.")

        self.func = func
        self.args = args or ()
        self.kwargs = kwargs or {}

    def catch(
        self,
        *exceptions: Type[Exception],
    ) -> Union[Tuple[Type[Exception], None], Tuple[None, T]]:
        """Catches provided exceptions if any occurs.

        Args:
            *exceptions (Type[Exception]): Variable length exceptions
            to catch.

        Returns:
            If no exception occurs, a `Tuple` of `(None, Value)`
            will be returned. Otherwise a `Tuple` of `(Exception, None)`
            will be returned. These can be accesses such as:

            `err, val = Try(some_func).catch(TypeError)`

        Raises:
            TypeError: If no exceptions provided.
        """

        if not exceptions:
            raise TypeError("At least one Exception required.")

        try:
            return (None, self.func(*self.args, **self.kwargs))
        except exceptions as err:
            return (err, None)

    async def async_catch(
        self,
        *exceptions: Type[Exception],
    ) -> Awaitable[Union[Tuple[Type[Exception], None], Tuple[None, T]]]:
        """Catches provided exceptions if any occurs. Async version of `catch`.

        Args:
            *exceptions (Type[Exception]): Variable length exceptions
            to catch.

        Returns:
            If no exception occurs, a `Tuple` of `(None, Value)`
            will be returned. Otherwise a `Tuple` of `(Exception, None)`
            will be returned. These can be accesses such as:

            `err, val = await Try(fetch).async_catch(HttpError)`

        Raises:
            TypeError: If no exceptions provided.
        """

        if not exceptions:
            raise TypeError("At least one Exception required.")

        try:
            return (None, await self.func(*self.args, **self.kwargs))
        except exceptions as err:
            return (err, None)
