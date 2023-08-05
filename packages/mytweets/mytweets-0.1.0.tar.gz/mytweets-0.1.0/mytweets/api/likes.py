import requests
import json


class MyLikes:
    def __init__(self, user_id, bearer_token) -> None:
        self.user_id = user_id
        self.bearer_token = bearer_token
    
    @staticmethod
    def __create_url(user_id):
        # Be sure to replace your-user-id with your own user ID or one of an authenticating user
        # You can find a user ID by using the user lookup endpoint
        # id = "your-user-id"
        id = user_id
        # You can adjust ids to include a single Tweets.
        # Or you can add to up to 100 comma-separated IDs
        url = "https://api.twitter.com/2/users/{}/liked_tweets".format(id)
        
        return url

    def bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2LikedTweetsPython"
        return r

    def connect_to_endpoint(self, 
                            url, 
                            max_results=100, 
                            tweet_fields='lang,author_id,created_at,entities', 
                            collect_all=True,
                            stop_if_collected_id_in=None,
                            verbose=False):
        
        # Tweet fields are adjustable.
        # Options include:
        # attachments, author_id, context_annotations,
        # conversation_id, created_at, entities, geo, id,
        # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
        # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
        # source, text, and withheld

        my_params = {'max_results':max_results, 'tweet.fields':tweet_fields}

        first_call = True
        response_dict = {'data':list(), 'meta':dict()}
        stop = False
        liked_tweets = list()
        while (first_call or 'next_token' in response_dict['meta']) and not stop:

            response = requests.request(
                "GET", url, auth=self.bearer_oauth, params=my_params)
            
            print(response.status_code)
            
            if response.status_code != 200:
                raise Exception(
                    "Request returned an error: {} {}".format(
                        response.status_code, response.text
                    )
                )
            
            if first_call:
                first_call = False

            # response_dict = json.loads(response.json())
            response_dict = response.json()
            
            if stop_if_collected_id_in is not None:
                X = set([x for x in stop_if_collected_id_in])
                Y = set([tweet['id'] for tweet in response_dict['data']])
                if not set(X).isdisjoint(Y):
                    stop = True

            liked_tweets += response_dict['data']

            if not collect_all:
                stop = True
        
        return liked_tweets

    def get_my_likes(self):
        url = self.__create_url(user_id=self.user_id)
        
        json_response = self.connect_to_endpoint(url)

        return json.dumps(json_response, indent=4, sort_keys=True)
    
    def get_last_k_likes(self, k=10):
        url = self.__create_url(user_id=self.user_id)
        
        json_response = self.connect_to_endpoint(url, max_results=k, collect_all=False)

        return json.dumps(json_response, indent=4, sort_keys=True)
    
    @staticmethod
    def save_json(json_response, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(json_response, f, ensure_ascii=False, indent=4)