import errors.cla_security as SecurityErrors
import errors.cla_rules as RuleErrors
import json
import os
import pprint
import requests
import ssl
import sqlite3
import time
import datetime

from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from security import VoterSecurity
from voter import Voter

dir_path = os.path.dirname(os.path.realpath(__file__))
auth_cert = os.path.join(dir_path, "auth.crt")
cla_cert = os.path.join(dir_path, "cla.crt")
cla_key = os.path.join(dir_path, "cla.key")
print("CLA running with cert {}".format(cla_cert))
print("CLA Cert found: ", os.path.isfile(cla_cert))
print("CLA Key found: ", os.path.isfile(cla_key))
print("Auth Cert found: ", os.path.isfile(auth_cert))

app = Flask(__name__)
CORS(app, resources={
    r"/": {"origins": "*"},
    r"/voters": {"origins": "http://digivote.cyber.stmarytx.edu"},
    r"/validate": {"origins": "https://ctf.cyber.stmarytx.edu"},
    r"/l*": {"origins": "*"}        
    })
voters = VoterSecurity()



def get_hit_count():
    try:
        app.counter += 1
    except:
        app.counter = 1
    return app.counter

@app.route('/')
def hello():
    count = get_hit_count()
    return 'CLA Server: Hello World! I have been seen {} times.\n'.format(count)

@app.route('/voters', methods=['GET'])
def get_voters():
    voter_list = voters.get_all_voters()
    if(request.args.get('only_participants') == "true"):
        response = requests.get("https://ctf.cyber.stmarytx.edu/polls/status",
            verify='auth.crt'
        )
        if response.status_code == 200 and json.loads(response.content).get("status") == "closed":
            voter_list = [ x for x in voter_list if x.has_voted ]
        else:
            abort(403, "Participants cannot be viewed until voting has closed.")
    return jsonify([{
        "firstName": voter.firstName,
        "lastName": voter.lastName,
        "birthdate": voter.birthdate.year,
        "city": voter.city,
        "state": voter.state,
        "zip": voter.zip,
        "gender": voter.gender,
        } for voter in voter_list])

@app.route('/voters', methods=['POST'])
def add_voter():
    try:
        if(request.args.get('fetch_user') == "true"):
            data = request.get_json()
            voter_list = voters.get_all_voters()
            voter_list = [x for x in voter_list if (
                x.firstName == data.get("firstName") and 
                x.lastName == data.get("lastName") and
                x.ssn == data.get("ssn") and
                x.birthdate == datetime.date(*[int(num) for num in data['birthdate'].split("-")])
            )]
            if len(voter_list) > 1:
                abort(500, "There was an internal issue: csp500")
            elif len(voter_list) < 1:
                abort(400, "Voter has not yet registered.")
            else:
                voter = voter_list[0]
                return jsonify({
                        "status": "registered",
                        "voter_id": voter.id,
                        "firstName": voter.firstName,
                        "lastName": voter.lastName,
                        "birthdate": voter.birthdate
                    })
        else:
            data = Voter.make_voter(request.get_json())
            data = voters.add_voter(data)
            response = jsonify({
                "status"  : "registered",
                "voter_id": data.id,
                "firstName": data.firstName,
                "lastName": data.lastName,
                "birthdate": data.birthdate
            })
            print("Added new Voter: ", response)
            return response
    except ValueError as ex:
        abort(400, ex)
    except RuleErrors.RuleException as ex:
        abort(403, ex)
    except SecurityErrors.SecurityException as ex:
        abort(401, ex)

@app.route('/validate', methods=['POST']) 
def validate_voter():
    data = request.get_json()
    if data is None or data.get("voter") is None or data.get("token") is None:
        abort(400, "Malformed input: fields `voter` and `token` required.")
    voter = voters.get_voter(data["voter"])
    if voter is None:
        abort(404, "Voter not found.")
    if (not voter.has_voted):
        response = requests.post(
            "https://ctf.cyber.stmarytx.edu/confirm",
            verify='auth.crt',
            json=data)
        if response.status_code == 200:
            if response.content is not None:
                voters.update_voter(voter.id, "has_voted", True)
                output = json.loads(response.content)
                output["cla"] = "validated"
                return jsonify(output)
            return abort(500, "Empty response from `confirm`")
        
    abort(400, "Unable to confirm vote.")


@app.route('/live')
def livenessCheck():
    return jsonify({"alive": "true"})

@app.route('/ready')
def readinessCheck():
    return jsonify({"ready": "true"})

if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('cla.crt', 'cla.key')
    app.run(host="0.0.0.0", port=443, debug=True, ssl_context=context)
