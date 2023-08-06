
class Flag:
    """
    This class represents a flag with a name.
    """
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    __repr__ = __str__


class ClassNamedFlag(Flag):
    """
    A :class:`Flag` named with the class name.
    """
    def __init__(self):
        super().__init__(self.__class__.__name__)
