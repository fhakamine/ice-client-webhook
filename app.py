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
        res = addUser(req)
    elif action == "modUser":
        res = modUser(req)
    elif action == "resetUser":
        res = resetUser(req)
    else:
        return {}

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def addUser(req):
    baseurl = "https://frederico-oktapreview-com-ep69yegp80gu.runscope.net/"
    key = "00McAPc46ptAbr4LnL3Gh7dwgutP4peA9u3A1xCH7c"
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
        speech = "User created"
    else:
        speech = "Error "+str(responsecode)
        #{"errorCode":"E0000001","errorSummary":"Api validation failed: login","errorLink":"E0000001","errorId":"oaeRG1lUiGZTPeCWKfB2s6avw","errorCauses":[{"errorSummary":"login: An object with this field already exists in the current organization"}]}

    # print(json.dumps(item, indent=4))
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-user-webhook-sample"
    }

def modUser(req):
    #define what to do based on the action parameter
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = makeYqlQuery(req)
    if yql_query is None:
        return {}
    yql_url = baseurl + urllib2.urlencode({'q': yql_query}) + "&format=json"
    #perform the rest api call
    result = urllib2.urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res

def resetUser(req):
    #define what to do based on the action parameter
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = makeYqlQuery(req)
    if yql_query is None:
        return {}
    yql_url = baseurl + urllib2.urlencode({'q': yql_query}) + "&format=json"
    #perform the rest api call
    result = urllib2.urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res

def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    #placeholder for variables
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))

    speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
             ", the temperature is " + condition.get('temp') + " " + units.get('temperature')

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
