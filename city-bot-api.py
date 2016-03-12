import flask
from flask import request
import redis
import collections
import json
import numpy as np
import time
import sys
import tweepy
from tweepy import OAuthHandler
import random
import StringIO

from flask import Flask, make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = flask.Flask(__name__)
conn1 = redis.Redis(db=1)
conn0 = redis.Redis(db=0)
count=0
c=0

def buildHistogram():
    keys = conn1.keys()
    dict={}
    for key in keys:
    	values = conn1.hgetall(key)
    	#print json.dumps({"valueeee": values})
    	#c = collections.Counter(values)
	#z = sum(c.values())
	#print z
    	for k,v in values.iteritems():
		#print json.dumps({"k": k, "v": v})
		if k in dict:
        		dict[k] += int(v)
    		else:
        		dict[k] = int(v)
    	z=sum(dict.values())
    
    return {k:v/float(z) for k,v in dict.iteritems()}

@app.route('/plot.png')
def plot():
    h=buildHistogram()
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    xs = range(len(h))
    ys = [x for k,x in h.iteritems()]

    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = StringIO.StringIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@app.route("/")
def histogram():
    h = buildHistogram()
    return json.dumps(h)

@app.route("/entropy")
def entropy():
    h = buildHistogram()
    return json.dumps({"sum":-sum([p*np.log(p) for p in h.values()])})

@app.route("/rate")
def rate():

    pipe = conn0.pipeline()
    keys = conn0.keys()
    avg_rate = 0
    #print keys
    if keys:
    	values = conn0.mget(keys)
    	try:
		rates = [float(v) for v in values]
		if len(rates):
			avg_rate = sum(rates)/float(len(rates))    		
    	except TypeError:
		print keys	
    return json.dumps({"avg_rate":avg_rate})
	    	
	    	

@app.route("/probability")
def probability():
    category = request.args.get('category', '')
    city = request.args.get('city', '')
    # get the distribution for the city
    print city
    print category
    d = conn1.hgetall(city)
    # get the count for the referrer
    print d
    try:
      m = d[category]
    except KeyError:
      return json.dumps({
        "city": city, 
        "prob": 0,
        "category": category
      })
    # get the normalising constant
    z = sum([float(v) for v in d.values()])
    return json.dumps({
      "city": city, 
      "prob": float(m)/z,
      "category": category
      })

    



if __name__ == "__main__":
    app.debug = True
    app.run()
