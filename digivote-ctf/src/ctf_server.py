import requests
import flask
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
import json
import os
import pprint
import ssl
import sqlite3
import time
import uuid
dir_path = os.path.dirname(os.path.realpath(__file__))
auth_cert = os.path.join(dir_path, "auth.crt")
ctf_cert = os.path.join(dir_path, "ctf.crt")
ctf_key = os.path.join(dir_path, "ctf.key")
print("CTF running with cert {}".format(ctf_cert))
print("CTF Cert found: ", os.path.isfile(ctf_cert))
print("CTF Key found: ", os.path.isfile(ctf_key))
print("Auth Cert found: ", os.path.isfile(auth_cert))
from flask import Flask, request, abort, jsonify

app = flask.Flask(__name__)
auth = HTTPBasicAuth()
CORS(app, resources={ 
    r"/hello.*": {"origins": "*"},
    r"/results.*": {"origins": "*"},
    r"/ballot.*": {"origins": "*"},
    r"/vote.*": {"origins": "*"},
    r"/polls.*": {"origins": "*"}
})
@auth.get_password
def validate_user(username):
    if username == "cyber":
        return "secure"
    return None


global counter
counter = 0
global pending_votes
pending_votes = dict()
global voter_votes
voter_votes = dict()
global votes
votes = dict()
global polls_open
polls_open = True

def get_hit_count():
    global counter
    counter += 1
    return counter

global ballot_items
ballot_items = [
        {
            "title":"Favorite Fruit",
            "options": [
                "Apple",
                "Banana",
                "Mango",
                "Orange",
                "Strawberry",
                "Peach"
            ]
        }, {
            "title":"Favorite Color",
            "options": [
                "Red",
                "Orange",
                "Yellow",
                "Green",
                "Blue",
                "Indigo",
                "Violet"
            ]
        }, {
            "title":"Best CPU Manufacturer",
            "options": [
                "AMD",
                "Intel"
            ]
        },{
            "title":"Best GPU Manufacturer",
            "options": [
                "AMD",
                "NVidia"
            ]
        }
    ]

@app.route('/ballot')
def getBallot():
    global ballot_items
    return flask.jsonify({"items": ballot_items})

global total_votes
total_votes = 0

def tally_vote(vote:dict):
    global total_votes
    global votes
    total_votes += 1

    for key, value in vote.items():
        if votes.get(key) is None:
            votes[key] = dict()
        if votes.get(key).get(value) is None:
            votes[key][value] = 0
        votes[key][value] += 1 

def remove_voter_votes(voter_id):
    global voter_votes
    global pending_votes
    votes = voter_votes.get(voter_id)
    if votes is not None:
        for vote_id in votes:
            index = str(voter_id) + str(vote_id)
            del pending_votes[index]
        del voter_votes[voter_id]


@app.route("/confirm", methods=["POST"])
def confirm_vote():
    data = request.get_json()
    if data.get("voter") is None or data.get("token") is None:
        abort(400, "Malformed Request: Missing information")
    index = str(data.get("voter") + data.get("token"))
    vote = pending_votes.get(index)
    if vote is None:
        abort(400, "Vote not found.")
    
    tally_vote(vote.get("form"))
    remove_voter_votes(str(data.get("voter")))
    return jsonify({
        "status": "accepted",
        "voter": data.get("voter"),
        "ctf": "confirmed" 
    })

def is_valid_ballot_selection(key, value):
    global ballot_items
    for item in ballot_items:
        if item["title"] == key:
            if value in item["options"]:
                return True

    return False

def validate_vote(vote:dict):
    data = request.get_json()
    token = uuid.uuid4()
    # make sure there's a voter in the vote
    if vote.get("voter") is None or vote.get("form") is None:
        abort(400, str(data))
    # make sure the values being passed are all valid
    for key, value in vote["form"].items():
        if not is_valid_ballot_selection(key, value):
            abort(400, "Invalid vote selection ... [{}]::{}".format(key, value))
    # store the vote in the temporaty table
    pending_votes[vote.get("voter") + str(token)] = vote
    if voter_votes.get(vote["voter"]) is None:
        voter_votes[vote["voter"]] = []
    # note that this voter has another vote.
    voter_votes[vote["voter"]].append(token) 
    response = requests.post(
        "https://cla.cyber.stmarytx.edu/validate",
        verify="auth.crt",
        json={
            "voter": data.get("voter"),
            "token": str(token)
        })
    if response.status_code == 200:
        return json.loads(response.content)
    del pending_votes[vote.get("voter") + str(token)]
    del voter_votes[vote["voter"]]
    abort(400, "Vote Rejected")

@app.route('/vote', methods=['POST'])
def cast_vote():
    global polls_open
    if polls_open is True:
        data = request.get_json()
        try:
            confirmation = validate_vote(data)
        except Exception as ex:
            abort(400, ex)
        if confirmation is not None:
            return jsonify(confirmation)
        else:
            return abort(500, "Internal Server Error")
    else:
        abort(403, "Voting has been closed.")

@app.route('/results', methods=["GET"])
def get_results():
    global polls_open
    if polls_open is True:
        abort(403, "Results are not available while polls are open.")
    else:
        return jsonify(votes)

@app.route('/polls/status', methods=["GET"])
def get_status():
    return jsonify({
        "status": "open" if polls_open else "closed"
    })

 
@app.route('/polls/<string:method>', methods=["POST"])
@auth.login_required
def manage_poll(method):
    global polls_open
    global votes
    if method in ("close", "open"):
        if "close" == method and polls_open is True:
            polls_open = False
            return flask.redirect("http://digivote.cyber.stmarytx.edu/election/results") 
        elif "open" == method and polls_open is False:
            votes = dict()
            polls_open = True
            return flask.redirect("http://digivote.cyber.stmarytx.edu/") 
    else:
        abort(400, "Invalid action")

@app.route

@app.route('/')
def hello():
    global polls_open
    return 'CTF Server :: The polls {}.'.format("are still open" if polls_open else "have been closed")


context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

if __name__ == "__main__":
    context.load_cert_chain(ctf_cert, ctf_key)   
    app.run(host="0.0.0.0", port=443, debug=True, ssl_context=context, threaded=True)