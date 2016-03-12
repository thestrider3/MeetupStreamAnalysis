import redis
import time
import json
conn1 = redis.Redis(db=1)

while True:

    cities = conn1.keys()

    for city in cities:


        d = conn1.hgetall(city)
	print d
        for category in d:
            if int(d[category]) > 1:
                count = int(d[category])
                count -= 1
                d[category] = str(count)
		print json.dumps({"cy": city,"category": category, "count": count})
        conn1.hmset(city,d)

    time.sleep(2)


