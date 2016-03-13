import json
import sys
import time
import redis
conn1 = redis.Redis(db=1)
lastArrival=0
conn0 = redis.Redis(db=0)

while 1:
    line = sys.stdin.readline()
    try:
        d = json.loads(line)
    except ValueError:
        # sometimes we get an empty line, so just skip it
        continue

    try:
        city = d['venue']['city']
    except KeyError:
        # if there is no city present in the message
        # then let's just ditch it
        continue

    try:
        category = d['group']['category']['name']
    except KeyError:
        # if there is no category defined in the message
        # then let's just ditch it
        continue

    try:
        members = d['yes_rsvp_count']
    except KeyError:
        # if there is no members who have rsvped yes in the message
        # then let's just ditch it
        continue 
    try:
        status = d['status']
    except KeyError:
        # if there is no status present in the message
        # then let's just ditch it
        continue 
    
    if status=='upcoming':     
	    conn1.hincrby(city, category, members)
	    print json.dumps({"city":city,"category":category, "members":members, "status":status})

	    t=float(time.time())
	    if lastArrival==0:
		lastArrival=t
		continue
	    delta=t-lastArrival
	    lastArrival=t
	    rate=1/delta
	    conn0.setex(t, rate, 120)
	    print json.dumps({"time":t, "rate": rate, "delta":delta})
	    sys.stdout.flush()
