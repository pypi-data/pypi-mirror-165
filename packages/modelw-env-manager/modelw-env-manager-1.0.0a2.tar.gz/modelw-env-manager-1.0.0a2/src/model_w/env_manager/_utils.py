import inspect


def loose_call(func, *args, **kwargs):
    """
    Lets you call a function using args and kwargs but won't throw an exception
    if one of the kwargs you mentioned wasn't actually as a parameter of the
    function.

    That's useful to do very basic dependency injection when writing a lib that
    calls handlers.

    Parameters
    ----------
    func
        The function you want to call
    args
        Args to bind
    kwargs
        Keyword args to bind
    """

    sig = inspect.signature(func)
    real_kwargs = {k: kwargs[k] for k in kwargs.keys() & sig.parameters.keys()}

    return func(*args, **real_kwargs)
