# import flask dependencies
from flask import Flask, request, make_response, jsonify
import intents

# initialize the flask app
app = Flask(__name__)


# default route
@app.route('/')
def index():
    return 'DialogFlow server is running!'


# function for responses
def results():
    # build a request object
    req = request.get_json(force=True)
    print(req)

    # fetch action from json
    action = req.get('queryResult').get('action')
    if action == "get-homework":
        answer, longans = intents.gethomework()
        if answer == "No":
            return {'fulfillmentText': longans}
        return {'fulfillmentText': longans}

    if action == 'add-homework':
        parameters = req.get('queryResult').get('parameters')
        print(parameters)
        ans = intents.addhomework(parameters)
        return (ans)

    # return a fulfillment response
    return {'fulfillmentText': 'This is a response from webhook.'}


# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))


# run the app
if __name__ == '__main__':
    app.run()
