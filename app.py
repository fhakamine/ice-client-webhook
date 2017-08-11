#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

import json
import os
import urllib
import requests

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

#INITIAL ROUTE
@app.route('/')
def itworks():
    return "I translate requests from API.AI to "+os.environ.get('PROMOS_API')+"/promos"

#POST:/WEBHOOK
@app.route('/webhook', methods=['POST'])
def webhook():
    #GET API.AI REQUEST
    req = request.get_json(silent=True, force=True)
    print("=== BEGIN: WHAT COMES FROM API AI? ===")
    print(json.dumps(req, indent=2))
    print("=== BEGIN: WHAT COMES FROM API AI? ===")

    #FIGURES OUT WHAT TO DO
    action = req.get("result").get("action")
    if action == "createPromos":
        speech = createPromos(req)
    elif action == "readPromos":
        speech = readPromos(req)
    elif action == "deletePromos":
        speech = deletePromos(req)
    else:
        speech = "I don't understand you."

    #RETURN RESPONSE
    res = {
            "speech": speech,
            "displayText": speech,
            "source": "apiai-user-webhook-sample"
          }
    res = json.dumps(res, indent=2)
    print("=== BEGIN: WHAT GOES BACK TO API AI? ===")
    print(res)
    print("=== BEGIN: WHAT GOES BACK TO API AI? ===")
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#FOR CREATING NEW PROMOS
def createPromos(req):
    speech = "Oops... I don't know how to create promos yet."
    return speech

#FOR DELETING EXISTING PROMOS
def deletePromos(req):
    speech = "Oops... I don't know how to delete promos yet."
    return speech

#FOR GETTING THE CURRENT PROMOS
def readPromos(req):
    promosApi = os.environ.get('PROMOS_API')
    promosUrl = promosApi+"/promos"
    parameters = req.get("result").get("parameters")
    promosUrl = promosUrl+"/"+parameters.get("target")
    querystring = {}
    payload = {}

    #LOOKING FOR AN ACCESS TOKEN
    access_token = req.get("originalRequest").get("data").get("user").get("accessToken")
    if !(access_token is None or access_token == "")
        headers={'Authorization': 'Bearer '+access_token }

    #CALL THE PROMOS API
    response = requests.get(promosUrl, json=payload, headers=headers, params=querystring)
    responsecode = response.status_code
    data = response.json()

    if responsecode == 200:
        #RETURN THE FIRST PROMO THAT SHOWS UP
        speech = "We a special promo. "+data[0].get("description")+". To get this promo, go to ice.cream.io and enter the code "+ data[0].get("code")
    else:
        speech = "Error "+str(responsecode)
    return speech

#LISTENER
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
