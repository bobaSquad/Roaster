# import flask dependencies
from flask import Flask, request, make_response, jsonify
import requests
# import intents

# initialize the flask app
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

    url = "https://graph.facebook.com/v7.0/me/messages?access_token=EAADeeYiPg2kBAEIhwcwH0Rr7fgpzeTgY625ycuF92q60J443tQGVlg6tjck5z3ZB8KfFuxyOa9jattaHZBtwHbP103V1mpAfGsyW7AbtDQjwAtTDYFKDBKV01ncFGI7CIeI3Asp94GoQU4kymocACpESZAY7PTkV6qZAZAu1kYEUhRZC5Gm23D"
    message_req = {"messaging_type": "", "recipient": {"id": ""}, "message": {
        "text": ""}}
    req = request.get_json(silent=True)
    intent = req['queryResult']['intent']['displayName']
    params = req['queryResult']['parameters']
    fb_prams = req['originalDetectIntentRequest']["payload"]["data"]
    sender = fb_prams["sender"]["id"]
    print(fb_prams)
    # if intent == 'get-homework':
    #     answer, longans = intents.gethomework()
    #     if answer == 'No':
    #         return {'fulfillmentText': longans}
    #     return {'fulfillmentText': longans}
    #
    # if intent == 'add-homework':
    #     parameters = req.get('queryResult').get('parameters')
    #     print(parameters)
    #     ans = intents.addhomework(parameters)
    #     return (ans)
    if intent == "init.cal":
        email = params["email"]
        message_req["messaging_type"] = "CONFIRMED_EVENT_UPDATE"
        message_req["recipient"]["id"] = sender
        message_req["message"]["text"] = "event is coming up soon! get ready!"\

        post_response = requests.post(url, json=message_req)
        print(post_response)
        return {'fulfillmentText': 'Calendar has been added! FFF'}

    return {'fulfillmentText': 'This is a response from webhook.'}


# run the app
if __name__ == '__main__':
    app.run()
