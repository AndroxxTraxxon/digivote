import sqlite3
import uuid
import voter

class VoterDAO:

    def __init__(self):
        self.voters = dict()

    def get_voter(self, voter_id: str):
        return self.voters[str(voter_id)]

    def add_voter(self, voter:voter.Voter):
        try:
            self.voters[str(voter.id)]
        except KeyError as e:
            self.voters[str(voter.id)] = voter
            return True
        raise ValueError("Voter with id {} already exists".format(str(voter.id)))

    def get_all_voters(self):
        return self.voters.values()
    
    def get_voters_who_voted(self):
        return [voter for voter in self.voters.values() if voter.has_voted]

