# luigi

![luigi](https://user-images.githubusercontent.com/23701803/138563799-8592360f-1bfc-415a-a8d4-455ca458e2bb.png)


Serve fresh copypasta sourced from Reddit to your Slack workspace.



## Setup

Setting up luigi is a 2-stage process.

### Creating credentials

Luigi requires some stuff to communicate with Reddit and Slack:
1. Clone the repository and copy `config.sample.json` to `config.json`.
2. Create a Slack app([instructions](https://api.slack.com/authentication/basics)) with the name "luigi". Enable [event subscriptions](https://api.slack.com/apis/connections/events-api) for your app and subscribe to the `app_mention` event. You will need to specify the URL where you plan to run luigi. If you intend to use localhost, use a  service like [ngrok](https://ngrok.com/) to tunnel your traffic to localhost through a public-facing URL. Finally, install the app to your workspace.
3. Copy the Bot User OAuth Token inside Installed App Settings to `slackbot_token` inside `config.json`. Now luigi is all set to respond to all `@` mentions in your workspace.
4. Go to [App Preferences](https://www.reddit.com/prefs/apps) in Reddit and create an app. Make sure to select `script`.
5. Copy the client id to `reddit_client_id` and client secret to `reddit_client_secret` inside `config.json`.
6. Finally, enter your reddit username and password in the `reddit_username` and `reddit_password` fields inside `config.json`. Now luigi is all set to serve pastas.


### Running luigi

1. Activate a python virtual environment.
2. Install python dependencies:
```console
foo@bar:~$ pip install -r requirements.txt
```
3. Copy `config.sample.json` to `config.json`. 
4. Run the web server:
```console
foo@bar:~$ python server.py
``` 

## Modes

Luigi operates in 2 modes:
- __regular mode:__ luigi will serve the latest unfiltered copypastas.
- __kiddie mode:__ luigi will filter the pastas to remove any NSFW content, to the best of its abilities. This is the default setting (to avoid any nasty surprises).

To turn off kiddie mode(and earn my eternal respect), set `kiddie_mode: False` inside `config.json`.


## Usage

Add luigi to a slack channel and mention it. Be prepared for colourful, utterly ridiculous, generally eye-bleach worthy content (especially without kiddie mode). Don't take it too seriously 🙂

*A random luigi post(because this README is looking too dry):*


![random_copypasta](https://user-images.githubusercontent.com/23701803/138563560-85f94d71-ac90-4be2-b577-8faa447201cd.png)
