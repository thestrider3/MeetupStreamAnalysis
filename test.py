
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
        entropy_prev=entropy
        if (entropy_diff>0.0001):
            time.sleep(5)
            auth=tweepy.OAuthHandler('D3tZyQU0mJq4sRKdS1pRPp9ir','270H9ONazxkZf0eLl0aC9AzB4Ln1sQqQ8SAwZQiAhj9bnPLAQD')
            auth.set_access_token('137228501-p7PCkPaD92n2nn4caokQd9loXz6ZGf2cZtdSpwpn','yro3A945UCSPeK0eUo1Yok9sd1uDH39RH5ghCFAJjgZPK')
            api = tweepy.API(auth)
            print api.me().name
            count=count+1
            tweet = "Entropy changed "+str(count)+"by "+str(entropy_diff)
            status = api.update_status(status=tweet)
        
