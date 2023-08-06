def decorator(fn):
    """
    Mark a function or a descriptor class as a decorator

    :param fn: a function or a class
    :return: marked function or class
    """
    fn.__is_decorator__ = True
    return fn


decorator.__is_decorator__ = True
