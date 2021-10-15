from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

@app.route('/',methods = ['POST'])
def respond():
    token = os.environ['SLACKBOT_TOKEN']

    content = request.json
    if "challenge" in content:
        challenge = content["challenge"]
        return jsonify({"challenge": challenge})

    if "event" in content:
        event = content["event"]
        if "type" in event:
            event_type = event["type"]
            print("Received event of type ", event_type)
            if event_type == "app_mention":
                channel_id = event["channel"]

                headers = {'Authorization': 'Bearer ' + token}
                r = requests.post('https://slack.com/api/chat.postMessage', headers=headers,
                data={"channel": channel_id, "text": "Hello world"})


    return jsonify(content)
    
if __name__ == "__main__":
    app.run(debug=True)