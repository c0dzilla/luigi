import requests, json, time, os
from random import randrange

config = json.load(open('config.json',))

def read_pasta_cache():
    pasta_cache_path = 'pasta_cache.json'
    if os.path.isfile(pasta_cache_path) and os.access(pasta_cache_path, os.R_OK):
        return json.load(open(pasta_cache_path))
    return None


def maybe_refresh():
    current_time = int(time.time())

    pasta_cache = read_pasta_cache()
    if pasta_cache is None:
        refresh(current_time)
        return

    last_refresh_time = pasta_cache.get('last_refresh_time')
    if (current_time - last_refresh_time >= config.get("pasta_refresh_interval_secs")):
        refresh(current_time)
        return

    # safety net in case previous refresh couldn't fetch pastas for some reason
    if len(pasta_cache.get('pastas')) == 0:
        refresh(current_time)


def refresh(current_time):
    pastas = []
    kiddie_indexes = []

    # setup auth to request reddit for an OAuth token
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

    limit = config.get("pasta_cache_count")
    if limit is None or limit >= 25:
        limit = 25
    params = {'limit': limit}

    res = requests.get("https://oauth.reddit.com/r/copypasta/new",
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

    pasta_cache = {
        'pastas': pastas,
        'kiddie_indexes': kiddie_indexes,
        'last_refresh_time': current_time
    }

    # update cache file
    with open('pasta_cache.json', 'w') as pasta_cache_file:
        print("Refreshing pasta cache at: ", current_time)
        json.dump(pasta_cache, pasta_cache_file)


def any_pasta():
    maybe_refresh()
    pasta_cache = read_pasta_cache()

    while pasta_cache is None:
        maybe_refresh()
        pasta_cache = read_pasta_cache()

    pastas = pasta_cache.get("pastas")
    return pastas[randrange(len(pastas))]


def any_kiddie_pasta():
    maybe_refresh()
    pasta_cache = read_pasta_cache()

    while pasta_cache is None:
        maybe_refresh()
        pasta_cache = read_pasta_cache()

    pastas = pasta_cache.get("pastas")
    kiddie_indexes = pasta_cache.get("kiddie_indexes")

    # no kiddie content available unfortunately, return without filter
    if len(kiddie_indexes) == 0:
        return pastas[randrange(len(pastas))]

    return pastas[kiddie_indexes[randrange(len(kiddie_indexes))]]
