class ExamineCardsPower(PresidentialPower):
    def __call__(self, president):
        pass # TODO

class NoPower(PresidentialPower):
    def __call__(self, president):
        pass

class PresidentialPower(object):
    def __call__(self, president):
        raise NotImplementedError("Each power needs the method to define what it does")
