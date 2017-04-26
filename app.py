#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

#from urllib.parse import urlparse, urlencode
#from urllib.request import urlopen, Request
#from urllib.error import HTTPError

import json
import os
import urllib2
import requests

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    #FIGURES OUT WHAT TO DO
    action = req.get("result").get("action")
    if action == "addUser":
        speech = addUser(req)
    elif action == "modUser":
        speech = modUser(req)
    elif action == "resetUser":
        speech = resetUser(req)
    else:
        return {}

    res = {
            "speech": speech,
            "displayText": speech,
            "source": "apiai-user-webhook-sample"
          }

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#for creating new users in Okta
def addUser(req):
    baseurl = os.environ.get('TENANT_URL')
    key = os.environ.get('API_KEY')
    url = baseurl+"/api/v1/users"

    result = req.get("result")
    parameters = result.get("parameters")
    firstName = parameters.get("given-name")
    lastName = parameters.get("last-name")
    email = parameters.get("email")

    querystring = {"activate":"true"}

    payload = {
        'profile': {
            'firstName': firstName,
            'lastName': lastName,
            'email': email,
            'login': email
            }
        }
    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'authorization': "SSWS "+key
        }

    response = requests.post(url, json=payload, headers=headers, params=querystring)

    print(response.text)
    print('After request')

    #perform the rest api call
    responsecode = response.status_code
    data = response.json()
    print(data)

    if responsecode == 200:
        speech = ""
    else:
        speech = "Error "+str(responsecode)

    print("Response:")
    print(speech)
    return speech

#for modifying existing users
def modUser(req):
    speech = "Ops... I don't know how to update a user yet."
    return speech

#for resetting users
def resetUser(req):
    speech = "Ops... I don't know how to reset users yet."
    return speech

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
