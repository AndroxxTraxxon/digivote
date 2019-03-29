import sqlite3
import uuid
import voter

class VoterDAO:
    def __init__(self):
        self.voters = dict()

    def get_voter(self, voter_id: uuid.UUID):
        if voter_id in self.voters:
            return self.voters[voter_id]
        return None

    def set_voter(self, voter:voter.Voter):
        self.voters[voter.id] = voter
        return voter

    def get_all_voters(self):
        return list(self.voters.values())
    
    def get_voters_who_voted(self):
        return [voter for voter in self.voters.values() if voter.has_voted]


