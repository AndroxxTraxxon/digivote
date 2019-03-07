from flask import Flask, request
from security import VoterSecurity
import json
import time
import ssl
import sqlite3
import voter

app = Flask(__name__)
global counter
counter = 0
voters = VoterSecurity()

def get_hit_count():
    global counter
    counter += 1
    return counter

@app.route('/voters', methods=['GET', 'POST'])
def handle_voters():
    if request.method == 'GET':
        voter_list = [{
                "firstName": voter.firstName,
                "lastName": voter.lastName,
                "birthDate": voter.birthDate} for voter in voters.get_all_voters()]
        return json.dumps(voter_list)
    elif request.method == 'POST':
        return json.dumps(voters.add_voter(
            voter.Voter.make_voter(
                request.get_json()
            )
        ))

@app.route('/voters/<uuid:voter_id>')
def get_voter(voter_id):
    return json.dumps(voters.get_voter(voter_id).__dict__)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'CLA Server: Hello World! I have been seen {} times.\n'.format(count)

@app.route('/live')
def livenessCheck():
    return json.dumps({"alive": "true"})

@app.route('/ready')
def readinessCheck():
    return json.dumps({"ready": "true"})

if __name__ == "__main__":
    context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('cla.crt', 'cla.key')
    app.run(host="0.0.0.0", port=443, debug=True, ssl_context=context)