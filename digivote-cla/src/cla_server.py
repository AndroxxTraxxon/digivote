import errors.cla_security as SecurityErrors
import errors.cla_rules as RuleErrors
import json
import os
import pprint
import requests
import ssl
import sqlite3
import time

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

@app.route('/voters')
def get_voters():
    voter_list = [{
        "firstName": voter.firstName,
        "lastName": voter.lastName,
        "birthDate": voter.birthDate} for voter in voters.get_all_voters()]
    if(request.args.get('only_participants') == "true"):
        voter_list = filter(lambda x: x.has_voted, voter_list)
    return jsonify(voter_list)



@app.route('/voters', methods=['POST'])
def add_voter():
    try:
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


@app.route('/voters/<uuid:voter_id>', methods=['GET'])
def get_voter(voter_id):
    return jsonify(voters.get_voter(voter_id))

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
    else:
        abort(400, "Voter has already voted.")


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
