# import flask dependencies
from flask import Flask, request, make_response, jsonify
import requests
from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from datetime import datetime
import intents
import pymongo


app = Flask(__name__)


# default route
@app.route('/', methods=['GET', "POST"])
def index():
    req = request.get_json(silent=True)
    return req if req is not None else {"Error": "JSON data not included in "
                                                 "request"}


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    return make_response(jsonify(results()))


def results():
    message_req = {
        "messaging_type": "",
        "recipient": {
            "id": ""
        },
        "message": {
            "text": ""
        }
    }
    url = "https://graph.facebook.com/v7.0/me/messages?access_token=EAADeeYiPg2kBAJ9JIGnbZAXW63zP3lmTw8B74suE4FcV2d2mZBkMSA9KII2fjYHRWtX40jVOT9YENgJx8bv3KtZBBFbhK3Bpmv4ynnag6K6ZCacUmD6nJt2kmZC9jkvcofYJmvsrqXwdK3BZAkfyOPo6zvHEq847T8mvYWqkJQZBkhPJvQhrGGx"
    req = request.get_json(silent=True)
    intent = req['queryResult']['intent']['displayName']
    params = req['queryResult']['parameters']
    fb_prams = req['originalDetectIntentRequest']["payload"]["data"]
    sender = fb_prams["sender"]["id"]
    if intent == 'get-homework':
        answer, longans = intents.gethomework()
        if answer == 'No':
            return {'fulfillmentText': longans}
        return {'fulfillmentText': longans}

    if intent == 'add-homework':
        parameters = req.get('queryResult').get('parameters')
        print(parameters)
        ans = intents.addhomework(parameters, sender)
        return (ans)
    if intent == "init.cal":
        email = params["email"]
        message_req["messaging_type"] = "CONFIRMED_EVENT_UPDATE"
        message_req["recipient"]["id"] = sender

        intents.get_events(email, url, message_req)
        client = pymongo.MongoClient(
            "mongodb+srv://eleezy99:jhopelover@fb-cluster-t7wyf.mongodb.net/reminders?retryWrites=true&w=majority")
        db = client.test
        print(db)
    # mydb = client.reminders
        mydb = client.reminders
        mycol = mydb.reminder_events
        # mydb=client['reminders']
        # mycol = mydb['reminders_col']
        mydict = {"user_id": sender, "email": email}
        x = mycol.insert_one(mydict)
        print(x.inserted_id)

        return {'fulfillmentText': 'Calendar has been added! FFF'}

    return {'fulfillmentText': 'This is a response from webhook.'}


# run the app
if __name__ == '__main__':
    app.run()
    url = "https://graph.facebook.com/v7.0/me/messages?access_token=EAADeeYiPg2kBAJ9JIGnbZAXW63zP3lmTw8B74suE4FcV2d2mZBkMSA9KII2fjYHRWtX40jVOT9YENgJx8bv3KtZBBFbhK3Bpmv4ynnag6K6ZCacUmD6nJt2kmZC9jkvcofYJmvsrqXwdK3BZAkfyOPo6zvHEq847T8mvYWqkJQZBkhPJvQhrGGx"

    client = pymongo.MongoClient(
        "mongodb+srv://eleezy99:jhopelover@fb-cluster-t7wyf.mongodb.net/reminders?retryWrites=true&w=majority")
    db = client.test
    mydb = client.reminders
    mycol = mydb.reminder_events

    res = mycol.find()
    email = params["email"]

    for doc in res:
        message_req = {
    "messaging_type": "",
    "recipient": {
        "id": ""
    },
    "message": {
        "text": ""
    }
        }

        user_id=doc['user_id']
        email=doc["email"]
        message_req["messaging_type"] = "CONFIRMED_EVENT_UPDATE"
        message_req["recipient"]["id"] = user_id
        print(email)
        print(user_id)
        intents.get_events(email, url, message_req)

