from flask import Flask, request
import json
import time
import ssl
import sqlite3
import dao
import voter

app = Flask(__name__)
global counter
counter = 0
dao = dao.CLADAO()

def get_hit_count():
    global counter
    counter += 1
    return counter

@app.route('/voters', methods=['GET', 'POST'])
def voters():
    if request.method == 'GET':
        voter_list = [{
                "firstName": voter.firstName,
                "lastName": voter.lastName,
                "birthDate": voter.birthDate} for voter in dao.get_all_voters()]
        return json.dumps(voter_list)
    elif request.method == 'POST':
        return json.dumps(dao.add_voter(
            voter.Voter.make_voter(
                request.get_json()
            )
        ))

@app.route('/voters/<uuid:voter_id>')
def get_voter(voter_id):
    return json.dumps(dao.get_voter(voter_id).__dict__)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'CLA Server: Hello World! I have been seen {} times.\n'.format(count)

if __name__ == "__main__":
    context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('cla.crt', 'cla.key')
    app.run(host="0.0.0.0", port=443, debug=True, ssl_context=context)