from typing import Any

from vr_configuration.printing.recursive_object_printing import \
    print_object_recursively


def print_config(
    config: Any,
) -> None:
    """
    Print a configuration object to the standard output.

    :param config: The configuration object to print.

    :return None
    """
    print_object_recursively(obj=config)
