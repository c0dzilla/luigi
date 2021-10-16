import requests
from flask import Flask, jsonify, request
from pasta_gen import any_pasta, any_kiddie_pasta

app = Flask(__name__)

@app.route('/',methods = ['POST'])
def respond():
    token = json.load(open('config.json',)).get("slackbot_token")

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
                data={"channel": channel_id, "text": any_pasta().get("selftext")})


    return jsonify(content)
    
if __name__ == "__main__":
    app.run(debug=True)