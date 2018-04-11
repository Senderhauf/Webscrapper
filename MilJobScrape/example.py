from bs4 import BeautifulSoup
	# imports the module BeautifulSoup4 - the most update 

import urllib.request
	# imports the module for opening urls via HTTP

def main():
	url = "https://milwaukee.craigslist.org/d/free-stuff/search/zip"
	
	html = urllib.request.urlopen(url)
		#html contains an HTTPResponse object

	soup = BeautifulSoup(html, "html.parser")

	print(soup.prettify())

if __name__ == '__main__':
	main()