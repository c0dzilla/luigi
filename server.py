import requests, json
from flask import Flask, jsonify, request
from pasta_gen import any_pasta, any_kiddie_pasta

app = Flask(__name__)

config = json.load(open('config.json',))

def send_pasta(channel_id):
    token = config.get("slackbot_token")
    headers = {'Authorization': 'Bearer ' + token}
    pasta_text = ""

    if config.get("kiddie_mode"):
        pasta_text = any_kiddie_pasta().get("selftext")
    else:
        pasta_text = any_pasta().get("selftext")

    r = requests.post('https://slack.com/api/chat.postMessage',
                      headers=headers,
                      data={"channel": channel_id, "text": any_pasta().get("selftext")})


@app.route('/',methods = ['POST'])
def respond():
    content = request.json

    if content is not None:
        # respond to slack's challenge
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
                    send_pasta(channel_id)

    return jsonify({"status": "ok"})
    
if __name__ == "__main__":
    app.run(debug=True)