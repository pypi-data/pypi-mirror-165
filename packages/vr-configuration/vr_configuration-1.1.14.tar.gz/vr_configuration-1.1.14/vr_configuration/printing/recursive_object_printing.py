from typing import Any

from vr_configuration.printing.recursive_dumping import dump_recursively


def print_object_recursively(
    obj: Any
) -> None:
    """
    Print an object to the standard output.

    :param obj: The object to print.

    :return None
    """

    print(
        dump_recursively(
            obj=obj,
        )
    )
