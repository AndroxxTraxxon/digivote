from .cla_base import CLAException
class RuleException (CLAException):
    """ Base Exception class for any CLA rule violations """
    pass

class VoterAlreadyExistsException(RuleException):
    pass