#This code snippted was taken from the Class Lecture taught by Professor Mike Dewar. In this file, the data obtained from 
#delta.py is parsed using JSON and the time and the difference delta is stored into Redis. The time is made the key as it 
#is unique and delta is attached to it as its value. A key expiration rate of 120 s is set in the method conn.setex() 
#which is sufficient for our purpose.
import json
import sys
import redis
lastArrival=0

conn0 = redis.Redis(db=0)



while 1:
    line = sys.stdin.readline()
    d = json.loads(line)
    time = d["time"]
    if lastArrival==0:
	lastArrival=time
	continue
    delta=time-lastArrival
    lastArrival=time
    rate=1/delta
    conn0.setex(time, rate, 120)
    print json.dumps({"time":time, "rate": rate, "delta":delta})
