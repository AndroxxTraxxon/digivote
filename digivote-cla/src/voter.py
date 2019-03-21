import datetime
import uuid

class Voter:
    globalVoterUUID = uuid.UUID('{79c5dfd0-e4f7-5a77-8486-c7030122d24c}')
    requiredFields = ['firstName', 'lastName', 'ssn', 'birthdate', 'state', 'city', 'zip']
    def __init__(
        self, **kwargs):
        for item in self.requiredFields:
            if item not in kwargs or item is None or item == "":
                raise ValueError("Voter requires field {}".format(item))
        self.firstName = kwargs['firstName']
        self.lastName = kwargs['lastName']
        self.ssn = kwargs['ssn']
        self.streetAddress = kwargs['streetAddress']
        self.city = kwargs['city']
        self.state = kwargs['state']
        self.zip = kwargs['zip']
        self.birthdate = datetime.date(*[int(num) for num in kwargs['birthdate'].split("-")])
        self.has_voted = False
        if 'has_voted' in kwargs:
            self.has_voted=kwargs['has_voted']
        self.id = uuid.uuid5(
            uuid.NAMESPACE_DNS,
            str(hash(self))
            )

    @classmethod
    def make_voter(cls, data):
        return cls(**data)

    def __hash__(self):
        return hash(str({
            "firstName": self.firstName.lower(),
            "lastName": self.lastName.lower(),
            "ssn": self.ssn,
            "birthdate": self.birthdate.isoformat(),
            "state": self.state.lower(),
            "city": self.city.lower()
        }))

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return "Voter(\'{lastName}, {firstName}\' born on {birthdate} from {city}, {state})".format(
                lastName=self.lastName,
                firstName=self.firstName,
                birthdate=self.birthdate,
                city=self.city,
                state=self.state
            )