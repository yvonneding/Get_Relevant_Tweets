import csv
import jsonlines
import glob
from tqdm import tqdm
with open("topics.csv") as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  key_topics = list(csv_reader)

extension = 'jsonl'
result = glob.glob('*.{}'.format(extension))
result.remove('users_meta_info.jsonl')
result.remove('barackobama_example.jsonl')


# for topic in key_topics:
#   relevant_tweets[topic[0]] = []

user_dict = {} # key: tweet_if, value: text
for user_file in tqdm(result):
  with jsonlines.open(user_file) as json_file:
    for line in json_file.iter():
      user_dict[line["tweet_id"]] = line['text']


for topic in tqdm(key_topics):
  with open(topic[0] + '.csv', 'w') as csv_file:
    fieldnames = ['tweet']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    # for user_file in result:
    #   # iterate through tweets for the user
    #   with jsonlines.open(user_file) as json_file:
    #     for line in json_file.iter():
    #       user_dict[line["tweet_id"]] = line['text']
    for key in user_dict:
      for each_phrase in topic:
        if each_phrase.lower() in user_dict[key].lower():
          writer.writerow({'tweet': user_dict[key]})
          break
  



# store jsonl as dictionary: key(id), value(text)
# for user in tqdm(result):
#   # print(user)
#   with jsonlines.open(user) as json_file:
#     for line in json_file.iter():
#       tweet = line["text"]
#       for topic in key_topics:
#         for each_phrase in topic:
#           if each_phrase.lower() in tweet.lower():
#             relevant_tweets[topic[0]].append(tweet)
#             break
#   # if len(relevant_tweets[topic[0]]) < 50:
#   #   print("The topic {} has less than 50 posts".format(topic))
# with open("relevant_tweet.csv", 'w') as csv_file:
#   fieldnames = ['topic', 'tweet']
#   writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
  
#   writer.writeheader()
#   for key in relevant_tweets:

#     writer.writerow({'topic': key, 'tweet': relevant_tweets[key]})
  
# print(relevant_tweets)