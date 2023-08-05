from typing import List, Optional


def _get_subconfig(
    *,
    config,
    attribute_path: Optional[List[str]],
) -> type:
    if attribute_path is None:
        return config

    for attribute_name in attribute_path:
        config = getattr(config, attribute_name)

    return config
