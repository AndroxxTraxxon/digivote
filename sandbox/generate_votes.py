import requests
import random
import pprint
import json

global street_names
street_names = ["Main Street", "Church Street",
"Main Street North",
"Main Street South",
"Elm Street",
"High Street",
"Main Street West",
"Washington Street",
"Main Street East",
"Park Avenue",
"2nd Street",
"Walnut Street",
"Chestnut Street",
"Maple Avenue",
"Maple Street",
"Broad Street",
"Oak Street",
"Center Street",
"Pine Street",
"River Road",
"Market Street",
"Water Street",
"Union Street",
"South Street",
"3rd Street",
"Park Street",
"Washington Avenue",
"Cherry Street",
"North Street",
"4th Street",
"Court Street",
"Highland Avenue",
"Mill Street",
"Franklin Street",
"Prospect Street",
"School Street",
"Spring Street",
"Central Avenue",
"1st Street",
"State Street",
"Front Street",
"West Street",
"Jefferson Street",
"Cedar Street",
"Jackson Street",
"Park Place",
"Bridge Street",
"Locust Street",
"Madison Avenue",
"Meadow Lane",
"Ridge Road",
"Spruce Street",
"5th Street",
"Grove Street",
"Pearl Street",
"Lincoln Street",
"Madison Street",
"Dogwood Drive",
"Lincoln Avenue",
"Pennsylvania Avenue",
"Pleasant Street",
"4th Street West",
"Adams Street",
"Jefferson Avenue",
"3rd Street West",
"7th Street",
"Academy Street",
"11th Street",
"2nd Avenue",
"East Street",
"Green Street",
"Hickory Lane",
"Route 1",
"Summit Avenue",
"Virginia Avenue",
"12th Street",
"5th Avenue",
"6th Street",
"9th Street",
"Charles Street",
"Cherry Lane",
"Elizabeth Street",
"Hill Street",
"River Street",
"10th Street",
"Colonial Drive",
"Valley Road",
"Winding Way",
"1st Avenue",
"Fairway Drive",
"Liberty Street",
"Monroe Street",
"2nd Street West",
"3rd Avenue",
"Broadway",
"Church Road",
"Delaware Avenue",
"Prospect Avenue",
"Route 30",
"Sunset Drive",
"Vine Street",
"Woodland Drive",
"6th Street West",
"Brookside Drive",
"Hillside Avenue",
"Lake Street",
"13th Street",
"4th Avenue",
"5th Street North",
"College Street",
"Dogwood Lane",
"Mill Road",
"7th Avenue",
"8th Street",
"Beech Street",
"Division Street",
"Harrison Street",
"Heather Lane",
"Lakeview Drive",
"Laurel Lane",
"New Street",
"Primrose Lane",
"Railroad Street",
"Willow Street",
"4th Street North",
"5th Street West",
"6th Avenue",
"Berkshire Drive",
"Circle Drive",
"Clinton Street",
"George Street",
"Hillcrest Drive",
"Hillside Drive",
"Laurel Street",
"Oak Lane",
"Park Drive",
"Penn Street",
"Railroad Avenue",
"Riverside Drive",
"Route 32",
"Route 6",
"Sherwood Drive",
"Summit Street",
"2nd Street East",
"6th Street North",
"Buckingham Drive",
"Cedar Lane",
"Creek Road",
"Durham Road",
"Elm Avenue",
"Fairview Avenue",
"Grant Street",
"Hamilton Street",
"Highland Drive",
"Holly Drive",
"King Street",
"Lafayette Avenue",
"Linden Street",
"Mulberry Street",
"Poplar Street",
"Ridge Avenue",
"7th Street East",
"Cambridge Court",
"Cambridge Drive",
"Clark Street",
"Essex Court",
"Franklin Avenue",
"Front Street North",
"Hilltop Road",
"James Street",
"Magnolia Drive",
"Myrtle Avenue",
"Route 10",
"Route 29",
"Shady Lane",
"Surrey Lane",
"Walnut Avenue",
"Warren Street",
"Williams Street",
"Wood Street"
]

global first_names 
first_names = [
  ("Olivia", "female"),
  ("Emma", "female"),
  ("Ava", "female"),
  ("Charlotte", "female"),
  ("Mia", "female"),
  ("Sophia", "female"),
  ("Isabella", "female"),
  ("Harper", "female"),
  ("Amelia", "female"),
  ("Evelyn", "female"),
  ("Noah", "male"),
  ("Liam", "male"),
  ("Benjamin", "male"),
  ("Oliver", "male"),
  ("William", "male"),
  ("James", "male"),
  ("Elijah", "male"),
  ("Lucas", "male"),
  ("Mason", "male"),
  ("Michael", "male")
]

def gen_streetAddr():
  global street_names
  return "{number} {street}".format(
    number = random.randint(0, 99999),
    street = random.choice(street_names)
  )

def gen_zip():
  return str(70000 + random.randint(0, 9999))

def gen_firstName():
  global first_names
  return random.choice(first_names)

global last_names
last_names = [
  "Smith",
  "Garcia",
  "Johnson",
  "Martinez",
  "Williams",
  "Rodriguez",
  "Jones",
  "Hernandez",
  "Brown",
  "Davis"
]

def gen_lastName():
  global last_names
  return random.choice(last_names)

global cities
cities = [
  ("San Antonio", "TX"),
  ("Houston", "TX"),
  ("Dallas", "TX"),
  ("Plano", "TX"),
  ("Fort Worth", "TX"),
  ("Helotes", "TX"),
  ("New Braunfels", "TX"),
  ("Corpus Christi", "TX"),
  ("El Paso", "TX"),
  ("Laredo", "TX"),
]

def gen_city():
  global cities
  return random.choice(cities) 

def gen_ssn():
  _0 = random.randint(0,999)
  _1 = random.randint(0,99)
  _2 = random.randint(0,9999)
  return "{0:0>3d}-{1:0>2d}-{2:0>4d}".format(_0, _1, _2)

def gen_birthdate():
  year = random.randint(1950, 2001)
  month = random.randint(1, 12)
  day = random.randint(1, 28)
  return "{}-{:0>2d}-{:0>2d}".format(year, month, day)

def gen_person():
  # firstName: "John",
  # lastName: "Smith",
  # ssn: "123-45-6789",
  # gender: "male",
  # streetAddress: "1234 Park Place Ave.",
  # city: "Boston",
  # state: "Hawaii",
  # zip: "12345",
  # birthdate: "1994-02-22"
  person = dict()
  person["firstName"], person["gender"] = gen_firstName()
  person["lastName"] = gen_lastName()
  person["streetAddress"] = gen_streetAddr()
  person["ssn"] = gen_ssn()
  person["city"], person["state"] = gen_city()
  person["zip"] = gen_zip()
  person["birthdate"] = gen_birthdate()
  return person

def registerVoter():
  voter = gen_person()
  response = requests.post(
      "https://cla.cyber.stmarytx.edu/voters",
      json = voter,
      verify ="auth.crt"
    )
  return response.json()["voter_id"]

def get_options():
  response = requests.get(
      "https://ctf.cyber.stmarytx.edu/ballot",
      verify ="auth.crt"
    )
  pprint.pprint(response.json())
  
  return response.json()

def submit_vote(voter_id, vote):
  payload = {
    "voter": voter_id,
    "form": vote
  }

  response = requests.post("https://ctf.cyber.stmarytx.edu/vote",
    json=payload,
    verify ="auth.crt"
  )


if __name__ == "__main__":
  ballot_options = get_options()["items"]
  for i in range(1000):
    voter_id = registerVoter()
    print("Registered Voter {}".format(voter_id))
    if random.random() < 0.95:
      vote = dict()
      for option in ballot_options:
        if random.random() < 0.9:
          vote[option["title"]] = random.choice(option["options"])
      submit_vote(voter_id, vote)
      print("Submitted Vote for {}".format(voter_id))
      pprint.pprint(vote)


  