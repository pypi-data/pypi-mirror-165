import base64
import hashlib
import os
import re
import json
import requests
from requests.auth import AuthBase, HTTPBasicAuth
from requests_oauthlib import OAuth2Session


class MyBookmarks:
    def __init__(self, client_id, client_secret, user_id=None) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

        self.access_token = None
        self.user_id = user_id

    def authorize(self, redirect_uri):

        # If you have selected a type of App that is a confidential client you will need to set a client secret.
        # Confidential Clients securely authenticate with the authorization server.

        # Inside your terminal you will need to set an enviornment variable
        # export CLIENT_SECRET='your-client-secret'

        # Remove the comment on the following line if you are using a confidential client
        # client_secret = os.environ.get("CLIENT_SECRET")

        # Replace the following URL with your callback URL, which can be obtained from your App's auth settings.
        redirect_uri = redirect_uri

        # Set the scopes
        scopes = ["bookmark.read", "tweet.read", "users.read", "offline.access"]

        # Create a code verifier
        code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
        code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)

        # Create a code challenge
        code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
        code_challenge = code_challenge.replace("=", "")

        # Start an OAuth 2.0 session
        oauth = OAuth2Session(self.client_id, redirect_uri=redirect_uri, scope=scopes)

        # Create an authorize URL
        auth_url = "https://twitter.com/i/oauth2/authorize"
        authorization_url, state = oauth.authorization_url(
            auth_url, code_challenge=code_challenge, code_challenge_method="S256"
        )

        # Visit the URL to authorize your App to make requests on behalf of a user
        print(
            "Visit the following URL to authorize your App on behalf of your Twitter handle in a browser:"
        )
        print(authorization_url)

        # Paste in your authorize URL to complete the request
        authorization_response = input(
            "Paste in the full URL after you've authorized your App:\n"
        )

        # Fetch your access token
        token_url = "https://api.twitter.com/2/oauth2/token"

        # The following line of code will only work if you are using a type of App that is a public client
        auth = False

        # If you are using a confidential client you will need to pass in basic encoding of your client ID and client secret.

        # Please remove the comment on the following line if you are using a type of App that is a confidential client
        auth = HTTPBasicAuth(self.client_id, self.client_secret)

        token = oauth.fetch_token(
            token_url=token_url,
            authorization_response=authorization_response,
            auth=auth,
            client_id=self.client_id,
            include_client_id=True,
            code_verifier=code_verifier,
        )

        # Your access token
        self.access_token = token["access_token"]
    
    def __get_user_id(self):

        # Make a request to the users/me endpoint to get your user ID
        user_me = requests.request(
            "GET",
            "https://api.twitter.com/2/users/me",
            headers={"Authorization": "Bearer {}".format(self.access_token)},
        ).json()
        self.user_id = user_me["data"]["id"]
    
    def __test_authorized(self):
        if self.access_token is None:
            redirect_uri = input(
            "Enter the redirect URL of your choice:\n"
            )
            self.authorize(redirect_uri=redirect_uri)
    
    def __test_user_id(self):
        if self.user_id is None:
            self.__get_user_id()
    
    def __test_ready_to_request(self):
        self.__test_authorized()
        self.__test_user_id()
    
    def get_my_bookmarks(self,
                        max_results=100, 
                        tweet_fields='lang,author_id,created_at,entities', 
                        collect_all=True,
                        stop_if_collected_id_in=None,
                        verbose=False):

        self.__test_ready_to_request()        

        # Make a request to the bookmarks url
        url = "https://api.twitter.com/2/users/{}/bookmarks".format(self.user_id)
        headers = {
            "Authorization": "Bearer {}".format(self.access_token),
            "User-Agent": "BookmarksSampleCode",
        }
        my_params = {'max_results':max_results, 'tweet.fields':tweet_fields}


        first_call = True
        response_dict = {'data':list(), 'meta':dict()}
        stop = False
        bookmarked_tweets = list()
        while (first_call or 'next_token' in response_dict['meta']) and not stop:

            response = requests.request("GET", url, headers=headers, params=my_params)

            print("Response code: {}".format(response.status_code))

            if response.status_code != 200:
                raise Exception(
                    "Request returned an error: {} {}".format(response.status_code, response.text)
                )
            
            if first_call:
                first_call = False

            response_dict = response.json()
            
            if stop_if_collected_id_in is not None:
                X = set([x for x in stop_if_collected_id_in])
                Y = set([tweet['id'] for tweet in response_dict['data']])
                if not set(X).isdisjoint(Y):
                    stop = True

            bookmarked_tweets += response_dict['data']

            if not collect_all:
                stop = True
            
            return bookmarked_tweets

    def get_last_k_bookmarks(self, k=10):
        
        json_response = self.get_my_bookmarks(max_results=k, collect_all=False)

        return json.dumps(json_response, indent=4, sort_keys=True)