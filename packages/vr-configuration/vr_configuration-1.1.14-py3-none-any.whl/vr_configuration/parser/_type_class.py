class _TypeableClass(object):
    def __init__(
        self,
        *,
        class_type: type,
    ):
        if not isinstance(class_type, type):
            raise TypeError()

        self._type: type = class_type
