from typing import Tuple

from vr_configuration.parser._type_class import _TypeableClass


def _create_type(
    *,
    type_name: str,
    attribute_names: Tuple[str, ...],
) -> type:
    if not isinstance(type_name, str):
        raise TypeError()

    if not isinstance(attribute_names, tuple):
        raise TypeError(
            f"Parameter {f'{attribute_names=}'.split('=')[0]} "
            f"needs to be of type {Tuple}, "
            f"but got {type(attribute_names)}."
        )

    for attribute in attribute_names:
        if not isinstance(attribute, str):
            raise TypeError()

    def __init__(self, **kwargs):
        for attribute_name, attribute_value in kwargs.items():
            if attribute_name not in attribute_names:
                raise KeyError(
                    f"Class {self.__class__.__name__} expected "
                    f"attribute names {attribute_names}, "
                    f"but got attribute named {attribute_name}."
                )

        for attribute_name, attribute_value in kwargs.items():
            setattr(self, attribute_name, attribute_value)

    created_type: type = type(
        type_name,
        (_TypeableClass,),
        {"__init__": __init__},
    )

    return created_type
