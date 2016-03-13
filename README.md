# MeetupStreamAnalysis
To calculate the rate, entopy and probabilities of different categories in meetup streaming API(stream.meetup.com)

In this assignment, I have chosen the Meetup API as my data source. Meetup provides a live HTTP stream of open events within public Meetup groups. The connection with client terminates only if there is server maintenance or a connection error. There is no authentication or parameter needed for connection to the stream and atmost 10 connections are allowed per client IP address.
 
The response obtained from the API is a HTTP chunk whose body is a single json object which is terminated by a newline.
New events are pushed into the stream when: 
  * a new event is created
  * a drafted event is published
  * the title, description, time, or venue of the event changes
  * the state of the event changes to or from canceled, deleted, upcoming, etc.

For a recurring event, the first instance as well as the next n instances of that event that fall within the next 20 days will be pushed to clients
Further information about the response of this method can be obtained from http://www.meetup.com/meetup_api/docs/stream/2/open_events/.

For this assignments, I have taken into consideration only those events which are upcoming. I am extracting the city, the category and the number of people who have RSVPed 'Yes' to the event from the stream. Out of these information, I am calculating the rate and the entropy of the stream as well as plotting the histogram of probabilities of number of people attending an event based on category. I am also calculating the probabilities of number of people attending an event  given a city and a category.
I have also created an alerting system based on change in entropy. The entropy changes when more people start attending events of a category which was initially less popular. I have set a threshold value of 0.001 in the change of entropy. This value is entirely observational. The alerts are posted as my tweets through my account. (https://twitter.com/tulika92)

In order to run this project
  * Step 1: Replace the Twitter API keys in the test.py file.
  * Step 2: Type redis-cli in your terminal to start the redis- server
  * Step 3: Write curl -i http://stream.meetup.com/2/open_events | python events_parse.py & python decrementer.py & python city-bot-api.py & python test.py in your terminal
  * Step 4: Go to localhost:5000, this page shows the categories along with their associated probabilities
  * Step 5: Go to localhost:5000/plot.png to view the histogram, localhost:5000/rate to see the average rate and localhost:5000/entropy to see the current entropy of the stream
  * Step 6: To view different categories present in a city, go to loacalhost:5000/citywithcategory
  * Step 7: In order to view the probability, go to localhost:5000/probability?city="city_name"&category="category_name" where city_name and category_name are the parameter of GET request.
