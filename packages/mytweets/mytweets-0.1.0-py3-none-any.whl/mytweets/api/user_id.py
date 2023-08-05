from requests_oauthlib import OAuth1Session
import json



class MyID:
    def __init__(self, consumer_key, consumer_secret) -> None:
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

        self.access_token = None
        self.access_token_secret = None

    
    def authorize(self):

        # Get request token
        request_token_url = "https://api.twitter.com/oauth/request_token"
        oauth = OAuth1Session(self.consumer_key, client_secret=self.consumer_secret)

        try:
            fetch_response = oauth.fetch_request_token(request_token_url)
        except ValueError:
            print(
                "There may have been an issue with the consumer_key or consumer_secret you entered."
            )

        resource_owner_key = fetch_response.get("oauth_token")
        resource_owner_secret = fetch_response.get("oauth_token_secret")
        print("Got OAuth token: %s" % resource_owner_key)

        # # Get authorization
        base_authorization_url = "https://api.twitter.com/oauth/authorize"
        authorization_url = oauth.authorization_url(base_authorization_url)
        print("Please go here and authorize: %s" % authorization_url)
        verifier = input("If you get a number, paste the PIN here, if not leave blank: ")
        if verifier == '':
            verifier = input("If you got redirected paste the complete URL here: ")
            verifier = verifier.split('oauth_verifier=')[-1]

        # Get the access token
        access_token_url = "https://api.twitter.com/oauth/access_token"
        oauth = OAuth1Session(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
            verifier=verifier,
        )
        oauth_tokens = oauth.fetch_access_token(access_token_url)

        self.access_token = oauth_tokens["oauth_token"]
        self.access_token_secret = oauth_tokens["oauth_token_secret"]

        return True

    def get_user_id(self, username, verbose=True):

        if self.access_token is None or self.access_token_secret is None:
            self.authorize()

        # User fields are adjustable, options include:
        # created_at, description, entities, id, location, name,
        # pinned_tweet_id, profile_image_url, protected,
        # public_metrics, url, username, verified, and withheld
        fields = "created_at,description"
        # params = {"usernames": "TwitterDev,TwitterAPI", "user.fields": fields}
        params = {"usernames": f"{username}", "user.fields": fields}

        # Make the request
        oauth = OAuth1Session(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret,
        )

        response = oauth.get(
            "https://api.twitter.com/2/users/by", params=params
        )

        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(response.status_code, response.text)
            )

        if verbose:
            print("Response code: {}".format(response.status_code))

        json_response = response.json()

        if verbose:
            print(json.dumps(json_response, indent=4, sort_keys=True))
        
        return json.dumps(json_response, indent=4, sort_keys=True)