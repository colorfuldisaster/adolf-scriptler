from singleton import *

class PresidentialPower(object):
    pass

class KillPower(PresidentialPower):
    __metaclass__ = Singleton

class SurpriseElectionPower(PresidentialPower):
    __metaclass__ = Singleton

class InvestigativePower(PresidentialPower):
    __metaclass__ = Singleton

class ExamineCardsPower(PresidentialPower):
    __metaclass__ = Singleton

class NoPower(PresidentialPower):
    __metaclass__ = Singleton
