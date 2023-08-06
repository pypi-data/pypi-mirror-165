
from typing import Iterator, TypeVar, Union, Type, Callable, Any

T = TypeVar('T')


def parse_args(args: list[str]) -> dict[str, Union[str, bool]]:
    res = {}  # type: dict[str, str | bool]
    for st in args:
        if st.startswith('-'):
            if '=' in st:
                key, *value = st.split('=')
                res[key] = '='.join(value)
            else:
                res[st] = True
    return res


def first(itr: Iterator[T]) -> Union[T, None]:
    try:
        return next(itr)
    except StopIteration:
        return None


def get_arg_types(func: Callable[..., Any]) -> Iterator[Type[T]]:
    annonations = getattr(func, '__annotations__', None) or {}  # type: dict[str, Type[T]]
    annonations.pop('return', None)
    yield from annonations.values()
