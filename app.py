#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

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
    if action == "createPromos":
        speech = createPromos(req)
    elif action == "readPromos":
        speech = readPromos(req)
    elif action == "deletePromos":
        speech = deletePromos(req)
    else:
        speech = "I don't understand you."

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
def createPromos(req):
    speech = "Oops... I don't know how to create promos yet."
    return speech

#for read existing promos
def readPromos(req):
    #getting environment variables
    promosApi = os.environ.get('PROMOS_API')
    promosUrl = promosApi+"/promos"

    parameters = req.get("result").get("parameters")
    promosUrl = promosUrl+"/"+parameters.get("target")
    #print('API Call')
    #print(promosUrl)

    querystring = {}
    payload = {}

    access_token = req.get("originalRequest").get("data").get("user").get("access_token")
    headers={'Authorization': 'Bearer '+access_token }
    #print(headers)

    #perform the rest api call
    response = requests.get(promosUrl, json=payload, headers=headers, params=querystring)

    #print('After request')
    responsecode = response.status_code
    data = response.json()
    #print(data)

    #for promo in data:
        #print("promo code: ");
        #print(promo);

    if responsecode == 200:
        speech = "We a special promo. "+data[0].get("description")+". To get this promo, go to ice.cream.io and enter the code "+ data[0].get("code")
    else:
        speech = "Error "+str(responsecode)

    print("Response:")
    print(speech)
    return speech

#for deleting promos
def deletePromos(req):
    speech = "Oops... I don't know how to reset users yet."
    return speech

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
