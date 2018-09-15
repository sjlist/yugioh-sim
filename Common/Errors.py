class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class ZoneError(Error):
    """" Exception for when a zone is full"""
    def __init__(self, message, zone, pile):
        self.message = message
        self.pile = pile
        self.zone = zone


class CardMissing(Error):
    """ Exception for when a card is missing from a pile """
    def __init__(self, message, card, pile):
        self.message = message
        self.pile = pile
        self.card = card


class PileError(Error):
    """ Exception for when a pile is not a valid pile """
    def __init__(self, pile):
        self.pile = pile


class InvalidOption(Error):
    """ Exception for invalid options passed in """
    def __init__(self, action, message):
        self.message = message
        self.action = action


class SummonError(Error):
    """ Exception thrown when an invalid summon is attempted """
    def __init__(self, message):
        self.message = message


class InvalidEffect(Error):
    """ Exception thrown when an invalid effect is attempted """
    def __init__(self, message):
        self.message = message