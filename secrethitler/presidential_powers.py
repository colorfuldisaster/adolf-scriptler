from .singleton import *

class PresidentialPower(object, metaclass=Singleton):
    pass

class KillPower(PresidentialPower):
    pass

class SurpriseElectionPower(PresidentialPower):
    pass

class InvestigativePower(PresidentialPower):
    pass

class ExamineCardsPower(PresidentialPower):
    pass

class NoPower(PresidentialPower):
    pass
