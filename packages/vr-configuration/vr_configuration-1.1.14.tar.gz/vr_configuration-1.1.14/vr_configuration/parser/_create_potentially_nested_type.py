from typing import Optional, Any, Dict

from vr_configuration.parser._create_type import _create_type


def _create_potentially_nested_type(
    attribute_name: Optional[str] = None,
    *,
    attribute_value: Any,
) -> type:
    attribute_name_str: str

    if attribute_name is None:
        if len(list(attribute_value.keys())) > 1:
            raise NotImplementedError(
                'Cannot handle multiple roots.'
                # YAML can, but that would not be a strict hierarchy
            )

        attribute_name_str = list(attribute_value.keys())[0]
        attribute_value = attribute_value[attribute_name_str]
    else:
        attribute_name_str = str(attribute_name)

    nested_type: type
    if isinstance(attribute_value, (dict, Dict)):
        nested_type = _create_type(
            type_name=attribute_name_str,
            attribute_names=tuple(attribute_value.keys()),
        )

        for attribute_name_str, attribute_value in attribute_value.items():
            nesting_type: type = _create_potentially_nested_type(
                attribute_name=attribute_name_str,
                attribute_value=attribute_value,
            )

            setattr(nested_type, attribute_name_str, nesting_type)
    else:
        nested_type = attribute_value

    return nested_type
