import json
import pprint
import ssl
import sqlite3
import time
import os
import errors.cla_rules as RuleErrors
import errors.cla_security as SecurityErrors

from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from security import VoterSecurity
from voter import Voter

dir_path = os.path.dirname(os.path.realpath(__file__))
auth_cert = os.path.join(dir_path, "auth.crt")
cla_cert = os.path.join(dir_path, "cla.crt")
cla_key = os.path.join(dir_path, "cla.key")

securedApp = Flask(__name__)
CORS(securedApp, resources={
  r"/secured/*": {"origins": "https://ctf.cyber.stmarytx.edu"}
  })

global counter
counter = 0
voters = VoterSecurity()

def get_hit_count():
  global counter
  counter += 1
  return counter


@securedApp.route('/secured/validate', methods=['POST'])
def validate_voter():
  data = request.get_json()
  print(data)
  if data is None:
    return jsonify({
      "status": "accepted",
    })
  else:
    data["status"] = "accepted"
    return jsonify(data)

@securedApp.route('/secured/live')
def securedLivenessCheck():
  return jsonify(
    {
      "host" : "cla_secured",
      "alive": "true"
    }
  )

@securedApp.route('/secured/ready')
def securedReadinessCheck():
  return jsonify({"ready": "true"})

def run():
  print("CLA SECURED running with cert {}".format(cla_cert))
  print("CLA SECURED Cert found: ", os.path.isfile(cla_cert))
  print("CLA SECURED Key found: ", os.path.isfile(cla_key))
  print("Auth Cert found: ", os.path.isfile(auth_cert))
  securedContext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
  securedContext.load_cert_chain('cla.crt', 'cla.key')
  securedContext.verify_mode = ssl.CERT_REQUIRED
  # securedContext.load_verify_locations(cafile='auth.crt')
  securedApp.run(host="0.0.0.0", port=4432, ssl_context=securedContext)
