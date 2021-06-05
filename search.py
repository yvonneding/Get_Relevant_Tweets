# topics = [["ab", "a", "bc"]]
# tweets = ["abc", "rwwed", "scccb"]
# relavant_tweet = []
# for topic in topics:
  
#   for tweet in tweets:
#     for each_phrase in topic:
#       if each_phrase in tweet:
#         relavant_tweet.append(tweet)
#         break
    

# print(relavant_tweet)
        
# import csv

# with open("topics.csv") as csv_file:
#   csv_reader = csv.reader(csv_file, delimiter=',')
#   # line_count = 0
#   # for row in csv_reader:
#   #   if line_count != 0:
#   key_topics = list(csv_reader)

#   print(key_topics)

# temp = {}
# temp["ab"].append(1)
# print(temp)
# topic = "today"
# print("the topic {} has less ".format(topic))

import json
test = [{"num": "8", "text": "today is good"}, {"num": "15", "text": "tomorrow is good"}]

with open("data.json", 'a') as f:
  for item in test:
    f.write(json.dumps(item) + '\n')

# watch ls -l data.json