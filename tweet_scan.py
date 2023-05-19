import configparser
import sys
from re import sub

import tweepy


class ConfigError(Exception):
    pass


class Scanner:
    """
    Class to scan new tweets on account Twitter.
    """

    def __init__(self, user=None):

        self.user = user
        # Read the config file and check that required values are present
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        # twitter
        self.__API_KEY = self.config['twitter']['api_key']
        self.__API_KEY_SECRET = self.config['twitter']['api_key_secret']
        self.__ACCESS_TOKEN = self.config['twitter']['access_token']
        self.__ACCESS_TOKEN_SECRET = self.config['twitter']['access_token_secret']

        self.__auth = None
        self.__api = None

        self.tweet_link = None
        self.tweet_text = None
        self.tweet_img = []

    def set_config(self):
        """
        Set new Twitter credentials in the config file if the token and id are not specified in the file.
        """

        self.config['twitter'] = {}
        self.config['twitter']['api_key'] = input("Enter your api_key: ")
        self.config['twitter']['api_key_secret'] = input("Enter your api_key_secret: ")
        self.config['twitter']['access_token'] = input("Enter your access_token: ")
        self.config['twitter']['access_token_secret'] = input("Enter your access_token_secret: ")
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def config_check(self):
        """
        Checking that Twitter credentials are present in the config file and raise an error in case of missing data.
        """
        if not (self.__API_KEY
                or self.__API_KEY_SECRET
                or self.__ACCESS_TOKEN
                or self.__ACCESS_TOKEN_SECRET):
            raise ConfigError

    def authenticate(self):
        self.__auth = tweepy.OAuth1UserHandler(
            consumer_key=self.__API_KEY,
            consumer_secret=self.__API_KEY_SECRET,
            access_token=self.__ACCESS_TOKEN,
            access_token_secret=self.__ACCESS_TOKEN_SECRET,
        )
        self.__api = tweepy.API(self.__auth)
        try:
            self.__api.verify_credentials()
            print("Authentication successful.")
        except tweepy.TweepyException as e:
            print(f"Authentication failed: {e}")
            sys.exit(1)

    def get_tweet(self):
        """
        Get the latest tweet from the user timeline.
        """
        # Get the current list of symbols
        username_object = self.__api.get_user(screen_name=self.user)

        # Get the latest tweet
        tweets = self.__api.user_timeline(
            user_id=username_object.id,
            screen_name=self.user,
            tweet_mode="extended",
            count=1
        )
        for tweet in tweets:
            self.tweet_link = tweet.id_str
            self.tweet_text = sub(r"https?://t.co[^,\s]+,?", "", tweet.full_text)
            self.tweet_img = []

            # Check for extended entities (e.g., images)
            if hasattr(tweet, "extended_entities"):
                entities = tweet.extended_entities
                if "media" in entities:
                    media = entities["media"]
                    for item in media:
                        if "media_url_https" in item:
                            self.tweet_img.append(item["media_url_https"])



