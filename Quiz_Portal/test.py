"""
This is a test module to check if Sphinx documentation is working properly
"""

def my_function(my_arg: int, my_other_arg:int):
    """
    Bla Bla Bla

    Parameters
    ----------
    my_arg : int
        A integer variable.
    my_other_arg : int
        Another integer variable.

    Returns
    -------
    int
        The sum of the two integers.

    Notes
    -----
    Bla Blu Bli Bla.

    Examples
    --------
    >>> my_function(1, 2)
    3
    """
    return my_arg + my_other_arg
