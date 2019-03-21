from data import VoterDAO
from errors import cla_rules
class VoterRules:
    def __init__(self, *args, **kwargs):
        self.voters = VoterDAO()

    def get_all_voters(self):
        return self.voters.get_all_voters()

    def get_voter(self, voter_id):
        return self.voters.get_voter(voter_id)

    def add_voter(self, voter):
        print("VoterRules.add_voter: ", voter)
        foundVoter = self.voters.get_voter(voter.id)
        print(foundVoter)
        if foundVoter is None:
            return self.voters.set_voter(voter)
        else:
            raise cla_rules.VoterAlreadyExistsException("{} already exists!".format(repr(voter)))