import requests, json, time
from random import randrange

config = json.load(open('config.json',))

pastas = []
kiddie_indexes = []
last_refresh_time = 0

def refresh(): 
    # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
    auth = requests.auth.HTTPBasicAuth(config.get("reddit_client_id"),
                                       config.get("reddit_client_secret"))

    # here we pass our login method (password), username, and password
    data = {'grant_type': 'password',
            'username': config.get("reddit_username"),
            'password': config.get("reddit_password")}

    # setup our header info, which gives reddit a brief description of our app
    headers = {'User-Agent': 'bot'}

    # send our request for an OAuth token
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)

    # convert response to JSON and pull access_token value
    TOKEN = res.json()['access_token']
    headers['Authorization'] = "bearer " + TOKEN

    params = {'limit': 10}

    # while the token is valid (~2 hours) we just add headers=headers to our requests
    res = requests.get("https://oauth.reddit.com/r/copypasta/top",
                    headers=headers,
                    params=params)

    # loop through each post retrieved from GET request
    for post in res.json()['data']['children']:
        # append relevant data to pastas
        pastas.append({
            'title': post['data']['title'],
            'selftext': post['data']['selftext'],
            'upvote_ratio': post['data']['upvote_ratio'],
            'ups': post['data']['ups'],
            'downs': post['data']['downs'],
            'score': post['data']['score'],
            'over_18': post['data']['over_18']
        })

        if not post['data']['over_18']:
            kiddie_indexes.append(len(pastas) - 1)


def maybe_refresh():
    current_time = int(time.time())
    if (current_time - last_refresh_time < config.get("pasta_refresh_interval_secs")):
        last_refresh_time = current_time
        refresh()

def any_pasta():
    maybe_refresh()
    return pastas[randrange(len(pastas))]

def any_kiddie_pasta():
    maybe_refresh()
    return pastas[kiddie_indexes[randrange(len(kiddie_indexes))]]

# refresh()
# print(any_pasta())
# print(any_kiddie_pasta())