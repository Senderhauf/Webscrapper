from bs4 import BeautifulSoup
	# imports the module BeautifulSoup4 - the most update 

import urllib.request
	# imports the module for opening urls via HTTP

import json





def get_listing_data(url, apt_list):
	listing = {
		'name': None, 
		'price': None, 
		'href': None, 
		'housing': None, 
		'location': None, 
		'available': None
	}

	html = urllib.request.urlopen(url)
	soup = BeautifulSoup(html, "html.parser")
	
	listing['price'] = int(soup.find("span", {"class":"price"}).get_text().replace("$",""))
	listing['name'] = soup.find("span", {"id":"titletextonly"}).get_text()
	listing['href'] = url 
	listing['housing'] = soup.find("span", {"class":"housing"}).get_text()
	listing['location'] = soup.find("div", {"class":"mapaddress"})
	if(not listing['location'] is None):
		listing['location'] = listing['location'].get_text()
	listing['available'] = soup.find("span", {"class":"housing_movein_now"})['data-date']

	apt_list.append(listing)
	
'''
def get_listings(url):
	html = urllib.request.urlopen(url)
	soup = BeautifulSoup(url, "html.parser")

	listingContainer = soup.findAll("li", {"class":"result-row"})

	for listing in listingContainer:
		get_listing_data()
'''

def main():
	url = "https://milwaukee.craigslist.org/search/apa?search_distance=2&postal=53211&max_price=600&min_bedrooms=1&max_bedrooms=2&availabilityMode=0&sale_date=all+dates"
	
	html = urllib.request.urlopen(url)
		#html contains an HTTPResponse object

	soup = BeautifulSoup(html, "html.parser")

	apartment_listings = []

	listingContainer = soup.findAll("li", {"class":"result-row"})

	for listing in listingContainer:
		print(listing.a["href"])
		get_listing_data(listing.a["href"], apartment_listings)

	apartment_listings = sorted(apartment_listings, key=lambda listing: listing['price'])
	
	for listing in apartment_listings:
		print('Price: {0}\nName: {1}\nHousing: {2}\nAvailable: {3}\nHref: {4}\n'.format(listing['price'], listing['name'], listing['housing'], listing['available'], listing['href']))

	with open("listings.txt", "w+") as outfile:
		for listing in apartment_listings:
			listing_json = json.dumps(listing)		
			outfile.write(str(listing_json))


if __name__ == '__main__':
	main()