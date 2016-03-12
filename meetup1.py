from __future__ import unicode_literals

import requests
import json
import time
import sys

def main():

        cities =[("New York","NY")]
        api_key= "3a4384d103343104c264bfd1215e"
        # Get your key here https://secure.meetup.com/meetup_api/key/
        for (city, state) in cities:
            
            offset = 0
            while True:
                response=get_results({"sign":"true","country":"US", "city":city, "state":state, "key":api_key,"offset":offset })
                time.sleep(1)
                offset += 1
                results_we_got = response['meta']['count']
                for group in response['results']:
                    category = ""
                    if "category" in group:
                        category = group['category']['name']
		    	print json.dumps({"time":float(time.time()),"city":city,"category":category, "members":group['members']})
			sys.stdout.flush()
            #time.sleep(1)



def get_results(params):
	request = requests.get("http://api.meetup.com/2/groups",params=params)
    	data = request.json()	
	return data


if __name__=="__main__":
        main()
