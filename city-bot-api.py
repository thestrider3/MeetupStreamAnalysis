#The code snippets were taken from E6998:Storytelling with Streaming Data class taught by Professor Mike Dewar. In this file, I am building an API as well as a webpage which provides information about the distribution by querying the API.
import flask
from flask import request
import redis
import json
import numpy as np
import StringIO
from collections import defaultdict
from flask import Flask, make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = flask.Flask(__name__)
conn1 = redis.Redis(db=1)
conn0 = redis.Redis(db=0)


#This function calculates the probabilities of the number of people attending an based on categories. The dict dictionary calculates the 
#number of people attending a particular categorical event and z is used to normalize the above calculation.
def buildHistogram():
    keys = conn1.keys()
    dict={}
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
    
    return {k:v/float(z) for k,v in dict.iteritems()}

#Here, the histogram is plotted using FigureCanvas which is then converted to a string and finally outputted as an png file.
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

#This serves as home page where the probability of each category with its category is displayed
@app.route("/")
def histogram():
    h = buildHistogram()
    return json.dumps(h)

#This is used to display the different categories of events occuring in a city
@app.route("/citywithcategory")
def city():
    keys = conn1.keys()
    city_dict = defaultdict(list)    
    for key in keys:
    	values = conn1.hgetall(key)
    	for k,v in values.iteritems():
		#print json.dumps({"k": k, "v": v})
		city_dict[key].append(k)    
    return json.dumps(city_dict)

#Here entropy is calculated by using its formula and values calculated in the buildHistogram function
@app.route("/entropy")
def entropy():
    h = buildHistogram()
    return json.dumps({"entropy":-sum([p*np.log(p) for p in h.values()])})

#Here, a moving average is calculated of the incoming stream.The rates are extracted from db0 and used to calculate averages. As, the rates expire every 120s, so the average rate reflects the average rate of current stream. If there is no data in the db0, which can happen if there is no events in the stream and all the previous keys have expired, then a zero is displayed.
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
    #print city
    #print category
    d = conn1.hgetall(city)
    # get the all the categories with number of members for each city
    print d
    try:
      m = d[category] #number of members attending an event in a particular category in a city, if the category mentioned in the get request doesn't belong to an upcoming event in the city, the probability is set to zero, otherwise the probability is calculated by divinding this number with total number of people attending any event in that city
      print m
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
