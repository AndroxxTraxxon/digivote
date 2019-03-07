from rules import VoterRules

class VoterSecurity:
    def __init__(self, *args, **kwargs):
        self.voters = VoterRules()

    def get_all_voters(self):
        return self.voters.get_all_voters()

    def add_voter(self, voter):
        return self.voters.add_voter(voter)

    def get_voter(self, voter_id):
        return self.voters.get_voter(voter_id)
