# Aly Saleh, 5th Dec 2021

# this file gets the keys that are returned by search_tweets function and stores them in status_keys.txt
# source: https://www.youtube.com/watch?v=ae62pHnBdAg
import sys

import tweepy
import json
import urllib3
import time
import socket

def tweets_writter_json(output_path, keyword, twitter_api, num_tweets):

    # the geocode is for approximately north america
    query = keyword + ' -filter:retweets'       #this removes retweets
    cursor = tweepy.Cursor(twitter_api.search_tweets, q=query, tweet_mode="extended", lang='en', result_type='recent').items(num_tweets)

    with open(output_path, 'w') as output_file:

        for tweet in cursor:                                   # cursor is an iterable object that contains the tweets
            tweet_string = json.dumps(tweet._json)
            output_file.write(tweet_string + '\n')             # this attribute contains all the details we require from the tweet


def main():

    tweepy.debug(True)      #to see the logs of the API, tells you how much API calss you have left

    auth = tweepy.OAuthHandler('1', '2')  # replace 1 with consumer key, replace 2 with consumer secret
    auth.set_access_token('1', '2')  # replace 1 with access token, replace 2 access token secret

    api = tweepy.API(auth, timeout=200)

    keywords200 = ['covid', 'vax', 'vaccination']
    keywords80 = ['moderna', 'astrazeneca', 'pfizer', 'johnson johnson', 'vaccine']

    for word in keywords200:
        file_path = '../data_no_retweets/' + word + '.txt'
        tweets_writter_json(file_path, word, api, 200)

    sys.exit()

    for word in keywords80:
        file_path = '../data_no_retweets/' + word + '.txt'
        tweets_writter_json(file_path, word, api, 80)


if __name__ == '__main__':
    main()
