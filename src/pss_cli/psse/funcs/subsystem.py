import typing
from itertools import groupby
from operator import itemgetter

attr_type = itemgetter(0)

if typing.TYPE_CHECKING:
    import psspy  # type: ignore


def subsystem_info(name, attributes, sid=-1, inservice=True):
    """
    Returns requested attributes from the PSS(r)E subsystem API
    for the given subsystem id and subsystem element name.

    e.g. to retrieve bus attributes "NAME", "NUMBER" and "PU"

      subsystem_info('bus', ["NAME", "NUMBER", "PU"])

    where the 'bus' `name` argument comes from the original
    PSS(r)E subsystem API naming convention found in Chapter 8 of the
    PSS(r)E API.

    abusint  # bus
    amachint # mach
    aloadint # load
    abrnint  # branch

    Args:
      inservice [optional]: True (default) to list only information
         for in service elements;
      sid [optional]: list only information for elements in this
         subsystem id (-1, all elements by default).

    """
    name = name.lower()
    gettypes = getattr(psspy, "a%stypes" % name)
    apilookup = {
        "I": getattr(psspy, "a%sint" % name),
        "R": getattr(psspy, "a%sreal" % name),
        "X": getattr(psspy, "a%scplx" % name),
        "C": getattr(psspy, "a%schar" % name),
    }

    result = []
    ierr, attr_types = gettypes(attributes)

    for k, group in groupby(zip(attr_types, attributes), key=attr_type):
        func = apilookup[k]
        strings = list(zip(*group)[1])
        ierr, res = func(sid, flag=1 if inservice else 2, string=strings)
        result.extend(res)

    return zip(*result)
