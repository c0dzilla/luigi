# luigi

![luigi](https://user-images.githubusercontent.com/23701803/138563799-8592360f-1bfc-415a-a8d4-455ca458e2bb.png)


Serve fresh copypasta sourced from Reddit to your Slack workspace.

Luigi maintains a local filesystem cache of copypastas that it keeps refreshing from new reddit posts on `r/copypasta`. The refresh rate and cache size are configurable (check config.sample.json). To increase the copypasta churn rate, prefer reducing the refresh interval over increasing the cache size.

*Note: This is a casual project written as a prototype and not intended for production-level deployments. For such cases, it can serve as a reference point.*

## Setup

Setting up luigi is a 2-stage process.

### Create credentials

Luigi requires some stuff to communicate with Reddit and Slack:
1. Clone the repository and copy config.sample.json to config.json.
2. Create a Slack app([instructions](https://api.slack.com/authentication/basics)) with the name "luigi". Enable [event subscriptions](https://api.slack.com/apis/connections/events-api) for your app and subscribe to the `app_mention` event. You will need to specify the URL where you plan to run luigi. If you intend to use localhost, use a  service like [ngrok](https://ngrok.com/) to tunnel your traffic to localhost through a public-facing URL. Finally, install the app to your workspace.
3. Copy the Bot User OAuth Token inside Installed App Settings to `slackbot_token` inside config.json. Now luigi is all set to respond to all `@` mentions in your workspace.
4. Go to [App Preferences](https://www.reddit.com/prefs/apps) in Reddit and create an app. Make sure to select `script`.
5. Copy the client id to `reddit_client_id` and client secret to `reddit_client_secret` inside config.json.
6. Finally, enter your reddit username and password in the `reddit_username` and `reddit_password` fields inside config.json. Now luigi is all set to serve pastas.


### Run luigi

1. Activate a python virtual environment.
2. Install python dependencies:
```console
foo@bar:~$ pip install -r requirements.txt
```
3. Run the web server:
```console
foo@bar:~$ python server.py
``` 

## Modes

Luigi operates in 2 modes:
- __Regular mode:__ luigi will serve the latest unfiltered copypastas.
- __Kiddie mode:__ luigi will filter the pastas to remove any NSFW content, to the best of its abilities. This is the default setting to avoid any nasty surprises.

To turn off kiddie mode (kudos, btw), set `kiddie_mode: false` inside config.json.


## Usage

Add luigi to a slack channel and mention it. Be prepared for colourful, utterly ridiculous, generally eye-bleach worthy content (especially without kiddie mode). Don't take it too seriously 🙂

*Couple of random luigi posts:*


![random_copypasta](https://user-images.githubusercontent.com/23701803/138563560-85f94d71-ac90-4be2-b577-8faa447201cd.png)

![random_copypasta](https://user-images.githubusercontent.com/23701803/138585426-a602692a-10e9-450b-b40e-602fff05d78c.png)


## Acknowledgements

This [blog](https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c) for a quick basic usage example of the Reddit API.
