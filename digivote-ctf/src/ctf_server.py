import requests
import flask
from flask_cors import CORS
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
CORS(app, resources={ 
    r"/hello.*": {"origins": "*"},
    r"/results.*": {"origins": "*"},
    r"/ballot.*": {"origins": "*"},
    r"/vote.*": {"origins": "*"}#"http://digivote.cyber.stmarytx.edu"}
})
global counter
counter = 0
pending_votes = dict()
votes = dict()

def get_hit_count():
    global counter
    counter += 1
    return counter


@app.route('/ballot')
def getBallot():
    return flask.jsonify([
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
    ])

global total_votes
total_votes = 0

def tally_vote(vote:dict):
    global total_votes
    total_votes += 1

    for key, value in vote.items():
        votes[key][value] += 1


@app.route
def confirm_vote():
    data = request.get_json()
    if data.get("voter") is None or data.get("token") is None:
        abort(400)
    index = str(data.get("voter") + data.get("token"))
    vote = pending_votes.get(index)
    if vote is None:
        abort(400)
    tally_vote(vote)
    return jsonify({
        "status": "accepted",
        "voter": data.get("voter") 
    })

def validate_vote(vote:dict):
    data = request.get_json()
    token = uuid.uuid4()
    if vote.get("voter") is None:
        abort(400)
    pending_votes[vote.get("voter") + str(token)] = vote
    response = requests.post(
        "https://cla.cyber.stmarytx.edu:4432/validate",
        verify="auth.crt",
        json={
            "voter": data.get("voter"),
            "token": str(token)
        })
    if response.status_code == 200:
        return True
    return False

@app.route('/vote', methods=['POST'])
def cast_vote():
    data = request.get_json()
    try:
        confirmation = validate_vote(data)
        
    except Exception as ex:
        abort(400, ex)
    if confirmation:
        return jsonify({
            "status": "accepted",
            "voter": data.get("voter")
        })
    else:
        abort(400, "vote rejected")

@app.route('/results', methods=["GET"])
def get_results():
    return jsonify(votes)

@app.route('/hello')
def hello():
    count = get_hit_count()
    return 'CTF Server:: Hello World! I have been seen {} times.\n'.format(count)


context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

if __name__ == "__main__":
    context.load_cert_chain(ctf_cert, ctf_key)   
    app.run(host="0.0.0.0", port=443, debug=True, ssl_context=context, threaded=True)