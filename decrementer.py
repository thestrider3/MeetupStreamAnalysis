#The code snippets were taken from E6998:Storytelling with Streaming Data class taught by Professor Mike Dewar. In this file, the data stored in db1 which is the number of people attending an event in each category in the city is decremented so that the effect of past values on the calculation of entropy as well as probability is used. Here, if the number of people attending an event is greater than one, then its value is decremented by 1% its initial value. This process is repeated every 10 seconds, so that our calculation always reflects present values as much as possible.
import redis
import time
import json
import math
conn1 = redis.Redis(db=1)

while True:

    cities = conn1.keys()

    for city in cities:


        d = conn1.hgetall(city)
	print d
        for category in d:
            if int(d[category]) > 1:
                count = int(d[category])
                count -= (0.01*count)
		count=int(math.floor(count))
                d[category] = str(count)
		print json.dumps({"cy": city,"category": category, "count": count})
        conn1.hmset(city,d)

    time.sleep(10)


