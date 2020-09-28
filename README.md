# Station-Updates
A project to run station departure boards on Twitter

Each station has a folder. Inside each is:
 - a tweeting v2.py file containing the code to get the data from the National Rail Darwin API and turn it into tweets.
 - an auth.py file (not included in this repositry) with the api keys to access the Twitter and National Rail Darwin APIs
 - the auth.py file should take the following form:
```
consumer_key        = ''
consumer_secret     = ''
access_token        = ''
access_token_secret = ''
rttapi_username     = ''
rttapi_password     = ''
nre_key             = ''
```
