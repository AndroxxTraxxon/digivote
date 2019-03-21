import requests
import flask
from flask_cors import CORS
import time
import ssl
import sqlite3
from flask import Flask, request, abort, jsonify

app = flask.Flask(__name__)
CORS(app, resources={ 
    r"/hello": {"origins": "*"},
    r"/results": {"origins": "*"},
    r"/ballot": {"origins": "*"},
    r"/vote": {"origins": "http://digivote.cyber.stmarytx.edu"}
})
global counter
counter = 0
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

def validate_voter_id(voter_id):
    requests.post(
        "https://cla.cyber.stmarytx.edu/validate", 
        verify= False, # "cla.crt",
        data={"id": voter_id}
        )

@app.route('/vote', methods=['POST'])
def cast_vote():
    data = request.get_json()
    validate_voter_id(data["voter_id"])
    for key, value in data["form"].items():
        print(key, value)
    return jsonify("Vote Submitted")

@app.route('/results', methods=["GET"])
def get_results():
    pass

@app.route('/hello')
def hello():
    count = get_hit_count()
    return 'CTF Server:: Hello World! I have been seen {} times.\n'.format(count)


context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('ctf.crt', 'ctf.key')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=443, debug=True, ssl_context=context)