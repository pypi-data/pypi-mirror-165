import re

def to_nth_str(i):
    """
    Converts an integer to a string like '1st', '2nd', '3rd', _etc_

    Parameters
    ----------
    i : int
        The integer to convert

    Returns
    -------
    str

    Examples
    --------

    Basic Usage:

    >>>
    >>> to_nth_str(21)  # -> "21st"
    >>> to_nth_str(2)   # -> "2nd"
    >>> to_nth_str(-11) # -> "-11th"
    >>>
    """
    if i in [11, 12, 13]:
        return f"{i}th"
    else:
        last = int(str(i)[-1])
        if last == 1:
            return f"{i}st"
        elif last == 2:
            return f"{i}nd"
        elif last == 3:
            return f"{i}rd"
        else:
            return f"{i}th"

def from_nth_str(s, ignore_case=True):
    """
    Converts a string like '1st', '2nd'... '4th', _etc_ to an integer

    To be specific, the exact pattern searched is:

        \b(-?[0-9]+)(st|nd|rd|th)\b

    Parameters
    ----------
    s : str
        The string to convert
    ignore_case : bool, optional
        Converts ``s`` to lowercase before processing

    Returns
    -------
    str, optional
        If successful, returns the converted string, otherwise returns None

    Examples
    --------

    Basic Usage:

    >>>
    >>> from_nth_str("1st")    # -> 1
    >>> from_nth_str("2nd")    # -> 2
    >>> from_nth_str("-103rd") # -> -103
    >>>

    On Failure:

    >>>
    >>> from_nth_str("1sttheworst") # -> None
    >>> from_nth_str("2ndthebest")  # -> None
    >>> from_nth_str("3rDtHePrInCeSsWiThThEhAiRyChEsT") # -> None
    >>>
    """
    s = s.lower() if ignore_case else s
    try:
        pttn = r"\b(-?[0-9]+)(st|nd|rd|th)\b"
        repl = r"\1"
        return int(re.sub(pttn, repl, s))
    except ValueError:
        return None

def neg_to_inf(x):
    """
    Returns 'infinite' if ``x < 0`` otherwise returns ``str(x)``

    Parameters
    ----------
    x : int | float
        The number to convert

    Returns
    -------
    str

    Examples
    --------

    Basic Usage:

    >>>
    >>> neg_to_inf(10)  # -> '10'
    >>> neg_to_inf(-1)  # -> 'infinite'
    >>>
    """
    return "infinite" if x < 0 else str(x)

def join(*args, sep=""):
    """
    Joins every item in ``args`` into a single ``str``

    Parameters
    ----------
    args : *any
        The items to join into a single string
    sep : str, optional
        A string to place between each item.
        Defaults to ''

    Returns
    -------
    str

    Examples
    --------

    Basic Usage:

    >>>
    >>> join(0, 1, 2)  # -> '012'
    >>> join(*['jam', 'marmalade', 'butter'], sep=' and ')  # -> 'jam and marmalade and butter'
    >>>
    """
    out = ""
    for i, arg in enumerate(args):
        out += str(arg)
        if i != len(args) - 1:
            out += str(sep)
    return out
