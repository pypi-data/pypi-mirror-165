from abc import ABC


class Traceable(ABC):
    """
    Traceable classes can be validated if the given url information is available.
    If the given url is not available the user is informed about it.
    """

    url: str
