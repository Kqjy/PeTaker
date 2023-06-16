from flask import Flask, render_template, request
from deta import Deta
from pet import Pet

import os
import json

deta = Deta(os.environ['DETA_PROJECT_KEY'])
petsdata = deta.Base('pets')
playerdata = deta.Base('player')
logsdata = deta.Base('logs')
app = Flask(__name__)
pet = Pet()

## Pages

@app.route('/', methods=["GET"])
def indexpage():
    try:
        pet.check()
        fetchData = petsdata.fetch().items
        data = pet.Decode(fetchData)
        return render_template("dashboard.html", data=data)
    except:
        return render_template("corrupted.html")

## API

@app.route('/api/view', methods=["POST"])
def viewdata():
    pet.check()
    fetchData = petsdata.fetch().items
    data = pet.Decode(fetchData)
    return data

@app.route('/api/logs', methods=["POST"])
def viewlogs():
    fetchData = logsdata.fetch().items
    fetchData = sorted(fetchData, key=lambda x: (x["timestamp"]), reverse=True)
    return fetchData

## Actions

@app.route('/actions/adopt', methods=["POST"])
@app.route('/actions/adopt/', methods=["POST"])
def action_adopt():
    getReq = request.data
    getReq = json.loads(getReq)
    type = getReq["type"]
    name = getReq["name"]
    if name and name.strip():
        message = pet.adopt(type, name)
    else:
        message = "Provide the pet a name!"
    return message

@app.route('/actions/view', methods=["POST"])
@app.route('/actions/view/', methods=["POST"])
def action_view():
    message = pet.view()
    return message

@app.route('/actions/pet', methods=["POST"])
@app.route('/actions/pet/', methods=["POST"])
def action_pet():
    message = pet.pet()
    return message

@app.route('/actions/play', methods=["POST"])
@app.route('/actions/play/', methods=["POST"])
def action_play():
    message = pet.play()
    return message

@app.route('/actions/wash', methods=["POST"])
@app.route('/actions/wash/', methods=["POST"])
def action_wash():
    message = pet.wash()
    return message

@app.route('/actions/feed', methods=["POST"])
@app.route('/actions/feed/', methods=["POST"])
def action_feed():
    message = pet.feed()
    return message

@app.route('/actions/abandon', methods=["POST"])
@app.route('/actions/abandon/', methods=["POST"])
def action_abandon():
    getReq = request.data
    getReq = json.loads(getReq)
    name = getReq["name"]
    message = pet.abandon(name)
    return message

@app.route('/__space/actions', methods=["GET"])
def metadata():
    return {
        "actions": [
            {
                "name": "adopt", 
                "title": "Adopt a pet", 
                "path": "/actions/adopt",
                "input": [
                    {
                        "name": "type",
                        "type": "string"
                    },
                    {
                        "name": "name",
                        "type": "string"
                    }
                ]
            },
            {
                "name": "view", 
                "title": "View pet status", 
                "path": "/actions/view"
            },
            {
                "name": "feed", 
                "title": "Feed your pet", 
                "path": "/actions/feed"
            },
            {
                "name": "wash", 
                "title": "Wash your pet", 
                "path": "/actions/wash"
            },
            {
                "name": "play", 
                "title": "Play with pet", 
                "path": "/actions/play"
            },
            {
                "name": "pet", 
                "title": "Pet your pet", 
                "path": "/actions/pet"
            },
            {
                "name": "abandon", 
                "title": "Abandon your pet", 
                "path": "/actions/abandon",
                "input": [
                    {
                        "name": "name",
                        "type": "string"
                    }
                ]
            }
        ]
    }

@app.route('/__space/v0/actions', methods=['POST'])
def actions():
  data = request.get_json()
  event = data['event']
  if event['id'] == 'cleanup':
    fetchData = logsdata.fetch().items
    if fetchData:
        for i in fetchData:
            logsdata.delete(i["key"])
        return "Cleared logs."
  return "Executed Action."