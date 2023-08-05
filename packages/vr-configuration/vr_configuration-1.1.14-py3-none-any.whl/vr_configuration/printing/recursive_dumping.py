from enum import Enum
from typing import Any


def dump_recursively(
    obj: Any,
    *,
    level: int = 0,
    dump_string: str = '',
) -> str:
    """
    Serialize any object to a string recursively.

    :return The string representing the given object.
    """

    if isinstance(obj, Enum):
        dump_string += \
            ' ' * level * 4 + obj.__class__.__name__ + ':' + '\n'
    else:
        dump_string += \
            ' ' * level * 4 + obj.__name__ + ':' + '\n'

    for attribute_name in dir(obj):
        if attribute_name in (
            '__abstractmethods__',
            '__annotations__',
            '__base__',
            '__bool__',
            '__call__',
            '__class__',
            '__contains__',
            '__delattr__',
            '__delete__',
            '__dict__',
            '__dir__',
            '__doc__',
            '__eq__',
            '__format__',
            '__ge__',
            '__get__',
            '__getattribute__',
            '__gt__',
            '__hash__',
            '__init__',
            '__init_subclass__',
            '__iter__',
            '__le__',
            '__lt__',
            '__module__',
            '__name__',
            '__ne__',
            '__new__',
            '__objclass__',
            '__qualname__',
            '__reduce__',
            '__reduce_ex__',
            '__repr__',
            '__self__',
            '__set__',
            '__setattr__',
            '__sizeof__',
            '__str__',
            '__subclasshook__',
            '__subclasshook__',
            '__text_signature__',
            '__weakref__',
        ):
            continue

        if isinstance(obj, Enum) and attribute_name == 'value':
            continue

        attribute_value = getattr(obj, attribute_name)
        if isinstance(
            attribute_value,
            (bool, dict, float, int, list, set, str, dict)
        ):
            dump_string += \
                ' ' * (level + 1) * 4 + \
                attribute_name + ': ' + \
                str(attribute_value) + '\n'
        else:
            dump_string = dump_recursively(
                obj=attribute_value,
                level=level + 1,
                dump_string=dump_string,
            )

    return dump_string
