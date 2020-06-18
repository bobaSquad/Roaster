# import flask dependencies
from flask import Flask, request, make_response, jsonify
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
    # build a request object
    req = request.get_json(silent=True)
    # fetch intent from json
    intent = req['queryResult']['intent']['displayName']
    params = req['queryResult']['parameters']
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
        return {'fulfillmentText': 'Calendar has been added! FFF'}

    
    # return a fulfillment response
    return {'fulfillmentText': 'This is a response from webhook.'}


# run the app
if __name__ == '__main__':
    app.run()
