import datetime
import uuid

class Voter:
    globalVoterUUID = uuid.uuid4()
    def __init__(
        self, 
        firstName='',
        lastName='',
        ssn='000-00-0000',
        streetAddress='',
        city='',
        state='',
        zip='00000',
        birthdate=datetime.datetime.now(),
        has_voted=False
        ):
        self.firstName = firstName
        self.lastName = lastName
        self.ssn = ssn
        self.streetAddress = streetAddress
        self.city = city
        self.state = state
        self.zip = zip
        self.birthdate = birthdate
        self.has_voted=has_voted
        self.id = uuid.uuid5(
            self.globalVoterUUID,
            firstName + lastName + ssn + str(birthdate)
            )

    @classmethod
    def init_class_uuid(cls, init_uuid: str):
        cls.globalVoterUUID = uuid.UUID(init_uuid)

    @classmethod
    def make_voter(cls, data):
        return cls(**data)