##The code snippets were taken from E6998:Storytelling with Streaming Data class. In this file, we are processing the response obtained from curling the meetup stream. Two redis databases are used. One is used for storing the timestamp of the incoming stream for calculating the rate of the stream. The other database is used to store the number of people attending an event of a particular category in the city.
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

####take only those events which are upcoming, ignore the canceled ones 
   
    if status=='upcoming':     
	    conn1.hincrby(city, category, members)
	    print json.dumps({"city":city,"category":category, "members":members, "status":status})
###increase the hash value of each category by the number of people attending that event
	    t=float(time.time())
	    if lastArrival==0:
		lastArrival=t
		continue
	    delta=t-lastArrival
	    lastArrival=t
	    rate=1/delta
###calculating rate as the inverse of the difference between the timestamp of two incoming stream event
	    conn0.setex(t, rate, 120)
####these values of rates are expired after 120 seconds so that the rate reflects the current rate of the stream rather than some past value
	    print json.dumps({"time":t, "rate": rate, "delta":delta})
	    sys.stdout.flush()
