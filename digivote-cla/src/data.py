import sqlite3
import uuid
from voter import Voter

class VoterDAO:
    def __init__(self):
        self.voters = dict()

    def get_voter(self, voter_id: uuid.UUID):
        if str(voter_id) in self.voters:
            return Voter.make_voter(self.voters[str(voter_id)])
        return None

    def set_voter(self, _voter:Voter):
        self.voters[str(_voter.id)] = _voter.__dict__
        return _voter

    def update_voter(self, voter_id, field_name, field_value):
        self.voters[str(voter_id)][field_name] = field_value

    def get_all_voters(self):
        return self.voters
    
    def get_voters_who_voted(self):
        return [Voter.make_voter(voter) for voter in self.voters.values() if Voter.make_voter(voter)]


