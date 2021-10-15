import requests, json

reddit_creds = json.load(open('reddit_creds.json',))

# note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
auth = requests.auth.HTTPBasicAuth(reddit_creds["client_id"],
                                   reddit_creds["client_secret"])

# here we pass our login method (password), username, and password
data = {'grant_type': 'password',
        'username': reddit_creds["username"],
        'password': reddit_creds["password"]}

# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'bot'}

# send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

# convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']
headers['Authorization'] = "bearer " + TOKEN

# while the token is valid (~2 hours) we just add headers=headers to our requests
res = requests.get("https://oauth.reddit.com/r/copypasta/top",
                   headers=headers)
