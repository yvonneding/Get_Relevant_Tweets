class Constants:
  url_twitter_follower = 'https://www.trackalytics.com/the-most-followed-twitter-profiles/page/{page_id}/'
  url_twitter_follower_max_page = 5
  # page ranges from 1~654, but people on the page after 450 don't have 10000 followers
  min_followers = 10000
  min_posts_per_topic = 50 # for qualitative analysis, for linguistic feature analysis, for our meeting discussion
  min_posts_per_topic_for_causal_inference = 500 # for do-calculus, propensity score matching

  csv_list_of_key_topics = 'topics.csv'  # 10-50 inspired from Joe Biden / Obama /
  # GovWhitmer (Michigan, Penn, Georgia, Wisconsin, 摇摆州)


class TwitterPosts:
  def __init__(self):
    self.twitter_id2followers = {}
    self.user_tweets = []
    self.set_twitter_ids()
    self.key_topics = []
    self.set_key_topics()  # a function to read csv
    self.extract_tweets()

  def set_key_topics(self):
    import csv

    with open("topics.csv") as csv_file:
      csv_reader = csv.reader(csv_file, delimiter=',')
      self.key_topics = list(csv_reader)
  
  def extract_tweets(self):
    from tqdm import tqdm
    for name, followers in tqdm(self.twitter_id2followers.items()):
      if int(followers) < C.min_followers:
        break
      self.get_all_tweets_by_id(name) # a list of posts (each post is a dict)

      # TODO: you can save this as a jsonl file
      # command: watch ls -l file_name
    relevant_tweets = {} # a dict with key=topic and value=list(relevant_tweet)
    for topic in self.key_topics:
      relevant_tweets[topic] = []
      for tweet in self.user_tweets:
        for each_phrase in topic:
          if each_phrase in tweet:
            relevant_tweets[topic].append(tweet)
            break
      if len(relevant_tweets[topic]) < C.min_posts_per_topic:
        print("The topic {} has less than 50 posts".format(topic))

  def get_all_tweets_by_id(self, twitter_name):
    # save jsonl
    # every tweet should keep the number of followers

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

    all_tweets = []
    tweets = api.user_timeline(screen_name=twitter_name, count=200)
    all_tweets.extend(tweets)

    oldest = all_tweets[-1].id - 1

    while len(tweets) > 0:
      tweets = api.user_timeline(screen_name=twitter_name, count=200, max_id=oldest)
      all_tweets.extend(tweets)
      oldest = all_tweets[-1].id - 1

    for tweet in all_tweets: 
      id = int(tweet.id_str)
      status = api.get_status(id)
      num_of_likes = status.favorite_count
      text = tweet.text.encode("utf-8")
      tweet_info = {"num_of_likes": num_of_likes, "text": text}
      self.user_tweets.append(tweet_info)

    with open("user_tweet.json", 'a') as jsonl_file:
      for tweet in self.user_tweets:
        jsonl_file.write(json.dumps(tweet) + '\n')
    
  def set_twitter_ids(self):
    from bs4 import BeautifulSoup
    import requests

    for page_id in range(1, C.url_twitter_follower_max_page + 1):
      url = C.url_twitter_follower.format(page_id=page_id)
      try:
        r = requests.get(url)
      except:
        continue

      soup = BeautifulSoup(r.text, 'html.parser')
      table = soup.find('table', class_ = 'table table-bordered table-striped')
      rows = table.tbody.find_all('tr')

      for row in rows:
        column = 0
        for td in row.find_all('td'):
          if column == 1:
            for href in td.find_all('a'):
              link = href['href']
              name = link.split('/')[-2]
          elif column == 2:
            follower = td.text.replace('\n', ' ').strip().split('(')[0]
            follower = follower.replace(',', '')
          column += 1
        self.twitter_id2followers[name] = follower

def main():
  tp = TwitterPosts()
  tp.extract_tweets()


if __name__ == '__main__':
  C = Constants
  main()
