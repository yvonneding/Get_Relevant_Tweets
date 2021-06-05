import tweepy
import csv
import json

# assign the values accordingly
consumer_key = "ilH6jnBJdh9HQdsufmygvUwMB"
consumer_secret = "LqErCdWfdP6BWf3LH3Q0RrJAXHoFvmweBUNtI1WljJ2A8SMelW"
access_token = "1181071568493056000-3TIQxUKR3FdFk2lzHBoCVsNmeS8UYF"
access_token_secret = "0amhncBmQXJY05SZ4VCQxG3CM4iZhElNrdtdxKL2Ux1la"
  
# authorization of consumer key and consumer secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  
# set access to user's access key and access secret 
auth.set_access_token(access_token, access_token_secret)
  
# calling the api 
api = tweepy.API(auth)

user_tweets = []

all_tweets = []
tweets = api.user_timeline(screen_name='barackobama', count=200)
all_tweets.extend(tweets)

oldest = all_tweets[-1].id - 1

while len(tweets) > 0:
  tweets = api.user_timeline(screen_name='barackobama', count=200, max_id=oldest)
  all_tweets.extend(tweets)
  oldest = all_tweets[-1].id - 1

for tweet in all_tweets: 
  id = int(tweet.id_str)
  status = api.get_status(id)
  num_of_likes = status.favorite_count
  text = tweet.text.encode("utf-8")
  tweet_info = {"num_of_likes": num_of_likes, "text": text}
  user_tweets.append(tweet_info)

with open("user_tweet.json", 'a') as jsonl_file:
  for tweet in user_tweets:
    jsonl_file.write(json.dumps(tweet) + '\n')