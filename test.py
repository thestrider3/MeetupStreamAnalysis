#The code snippets were taken from E6998:Storytelling with Streaming Data class. In this file, I have created an alerting system.
#I am monitoring the entropy of the stream; if the entropy changes by 0.001, then a tweet is posted through my account. This entropy 
#change signifies that more people are now going to events based on category which were less popular.
import redis
import json
import time
import sys
import tweepy
from tweepy import OAuthHandler
import numpy as np
conn1 = redis.Redis(db=1)
count=0
entropy_prev=0

while 1:

    pipe = conn1.pipeline()
    keys = conn1.keys()
    dict={}
    if keys:
        for key in keys:
        
            values = conn1.hgetall(key)
            #print json.dumps({"valueeee": values})
            for k,v in values.iteritems():
                #print json.dumps({"k": k, "v": v})
                if k in dict:
                    dict[k] += int(v)
                else:
                    dict[k] = int(v)
            z=sum(dict.values())
        
        
        h={k:v/float(z) for k,v in dict.iteritems()}
        entropy=-sum([p*np.log(p) for p in h.values()])
        entropy_diff=entropy-entropy_prev
        if (entropy_diff>0.001 and int(entropy_prev)!=0):
            time.sleep(5)
            auth=tweepy.OAuthHandler('Consumer Key','Consumer Sceret Key')
            auth.set_access_token('Access Key','Access Secret Key')
            api = tweepy.API(auth)
            print api.me().name
            count=count+1
            tweet = "Entropy changed "+str(count)+"by "+str(entropy_diff)
            status = api.update_status(status=tweet)
        entropy_prev=entropy
