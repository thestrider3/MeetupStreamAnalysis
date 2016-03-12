import json
import sys
import redis
import time
import urlparse

conn1 = redis.Redis(db=1)

while 1:
    line = sys.stdin.readline()
    try:
        d = json.loads(line)
    except ValueError:
        # sometimes we get an empty line, so just skip it
        continue

    try:
        city = d["city"]
    except KeyError:
        # if there is no city present in the message
        # then let's just ditch it
        continue

    try:
        category = d["category"]
    except KeyError:
        # if there is no referrer present in the message
        # then let's just ditch it
        continue
    try:
        members = d["members"]
    except KeyError:
        # if there is no referrer present in the message
        # then let's just ditch it
        continue

    conn1.hincrby(city, category, 1)
    print json.dumps({"cy": city, "category":category,"members": members})
    sys.stdout.flush()
