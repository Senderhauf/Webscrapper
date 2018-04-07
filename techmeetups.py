#!/usr/bin/python3 
print("Content-type:text/html\r\n\r\n")
print("<html>")
print("<head><title>Webscrapped Tech Events</title></head>")
print("<body>")
print("<h1> Other Tech Events Near You: </h1>")

import cgi


'''
Webcrawler Ideas:
        Goal: Create webcrawler app for other local techevents to be added to the IEEE CS website
        Ideas:
                Local Events for coders from various sites such as:
                        https://www.eventbrite.com/d/wi--milwaukee/free--science-and-tech--events/?crt=regular&sort=best
                        http://newaukee.com/event/open-source-showcasing-milwaukees-engineering-culture/
                        https://www.meetup.com/find/events/tech/?allMeetups=false&radius=10&userFreeform=Milwaukee%2C+WI&mcId=z53211&mcName=Milwaukee%2C+WI&eventFilter=all
'''
#webcrape python program with BeautifulSoup package


#import beautiful soup v4
import bs4
import re
from datetime import datetime
import dateparser
#Webclient to grab urls from Internet
#Need package urllib package, modularize urllib to get module request
#Function urlopen defined as uReq

from urllib.request import urlopen as uReq

from bs4 import BeautifulSoup as soup #modularize bs4 

'''
create a list of defined event dictionary
parse the date and time to an integer value 
set keys of event and add events to 

'''

event = {
	'date_time': None,
	'host_venue': None,
	'name': None,
	'url': None	
}

eventList = []

#filename = "meetup_tech_webscrap.csv"
#f = open(filename, "w")

############################################################################################

my_url = "https://www.meetup.com/find/events/tech/?allMeetups=false&radius=50&userFreeform=Milwaukee%2C+WI&mcId=z53211&mcName=Milwaukee%2C+WI&eventFilter=all";
uClient = uReq(my_url)

page_html = uClient.read() #save the html data from read() into "page_html"

uClient.close() #close webclient due to open internet connection

page_soup = soup(page_html, "html.parser") #call soup fxn to parse html data as html file 

eventContainers = page_soup.findAll("ul", {"class":"event-listing-container"})

#eventContainers contains an array of event dates
#LOOP: for each event date place events into container named "eventListingContianer"
#eventListingContainer = eventContainers[0]

headers = "date/time, host/venue, name, url\n"

#f.write(headers)

for eventListingContainer in eventContainers:

	event_day = eventListingContainer.findAll("li",{"class":re.compile("event-listing")})

	#len(event_day) is the number of events in particular day

	for event in event_day:
		year = event["data-year"]
		day = event["data-day"]
		month = event["data-month"]

		date = str(month)+"/"+str(day)+"/"+str(year)

		time = event.find("time",{"itemprop":"startDate"}).text

		host = event.find("div",{"class":"chunk"}).div.a.span.text

		name = event.find("a",{"class":re.compile("wrapNice")}).span.text

		url = event.find("a",{"class":re.compile("wrapNice")})["href"]

		event['date_time'] = dateparser.parse(date + " " + time)

		event['host_venue'] = host
		event['name'] = name
		event['url'] = url
		eventList.append(event)

#		f.write(date + " " + time + "," + host +","+ name + ","+ url + "\n")

###################################################################################################################

my_url = 'https://www.eventbrite.com/d/wi--milwaukee/free--science-and-tech--events/?crt=regular&sort=best'

uClient = uReq(my_url)

page_html = uClient.read() #save html data before closing webclient

uClient.close() 

page_soup = soup(page_html, "html.parser")

#f = open(filename, "a")

events = page_soup.findAll("div", {"class":re.compile("list-card-v2")})


for event in events:

	date_time = event.find("time", {"class":"list-card__date"}).text.strip()
	host = event.find("div", {"class":"list-card__venue"}).text.strip()
	name = event.find("div", {"class":"list-card__title"}).text.strip()
	url = event.a["href"]

	date_time = date_time.replace('\n','') #formatting defunkyfied 
	date_time = date_time.replace("           ",'') #formatting was funky before

	if dateparser.parse(date_time) > dateparser.parse('now'):
		event['date_time'] = dateparser.parse(date_time)

		event['host_venue'] = host
		event['name'] = name
		event['url'] = url
		eventList.append(event)

#		f.write(date_time + "," + host + "," + name + "," + url + "\n")

###################################################################################################################
eventList = sorted(eventList, key=lambda event: event['date_time'])

for event in eventList:
	print("<p>Date & Time: "+str(event['date_time'])+"</p>")
	print("<p>Event: "+event['host_venue']+"</p>")
	print("<p>Name: "+event['name']+"</p>")
	print("<p>Url: "+event['url']+"</p")
	print("<br>")
	print("<br>")

print("</body>")
print("</html>")
#f.close()



