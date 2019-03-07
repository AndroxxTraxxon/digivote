import VoterDAO from data

class VoterRules:
    def __init__(self, *args, **kwargs):
        self.voters = VoterDAO()

    def get_all_voters(self):
        return self.voters.get_all_voters()