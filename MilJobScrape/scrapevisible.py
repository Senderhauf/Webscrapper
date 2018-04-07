from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import re
import html as htmlmodule

def tag_visible(element):
	if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
		return False
	if isinstance(element, Comment):
		return False
	return True

def text_from_html(body):
	soup = BeautifulSoup(body, 'html.parser')
	texts = soup.findAll(text=True)
	visible_texts = filter(tag_visible, texts)
	html_text = u" ".join(t.strip() for t in visible_texts)
	#html_text = html_text.replace('\n', ' ').replace('\r', ' ') #remove newline and carraige return for regex parsing, '.' matches any char except a newline 
	html_text = re.sub('log\sin.*home\sfind\sa\sjob', '', html_text, flags=(re.IGNORECASE|re.DOTALL))
	html_text = re.sub('email\sthis\sjob.*all\srights\sreserved', '', html_text, flags=(re.IGNORECASE|re.DOTALL))

	return html_text


def post_to_file(my_url, filename):
	f = open(filename, "w+")
	html = urllib.request.urlopen(my_url)
	f.write(text_from_html(html))


def get_jobs(jobs_url):
	html = urllib.request.urlopen(jobs_url)
	soup = BeautifulSoup(html, "html.parser")

	jobsContainer = soup.findAll("div", {"class":"isg-job-summary-section"})

	for listing in jobsContainer:
		jobDetail = listing.div.div.div.div.a
		filename = jobDetail["title"]
		filename = filename.replace('/', '')
		filename = filename.replace(' ', '_')
		filename += '.txt'
		print(filename)
		post_to_file('https://www.milwaukeejobs.com' + jobDetail["href"], filename)

def main():
	#jobs_url = input("Enter milwaukeejobs url: ")
	keywords = input("Enter Search Keywords: ")
	keywords.strip()
	keywords = keywords.replace(' ', '+')
	jobs_url = 'https://www.milwaukeejobs.com/jobs.asp?pagemode=13&nav=2&page=1&pf=1&agent_category_id=-1&pbid=-1&job_code=-1&category_id=-1&company_id=&job_type_id=3&city_id=-1&location_id_1=31&location_type_1=C&location_name_1=Milwaukee,%20WI&location_radius_1=50&location_id_2=&location_type_2=&location_name_2=&location_radius_2=50&location_id_3=&location_type_3=&location_name_3=&location_radius_3=50&domain_id=-1&keywords='+keywords+'&order_by=relevance&direction=DESC&date_field=updated&changed=-1&is_staff_provider=-1&experience_years_min=-1&experience_years_max=-1&wage_class=-1&security_clearance_id=-1&co_id_int_list=&is_federal_contractor=-1'
	html = urllib.request.urlopen(jobs_url)
	soup = BeautifulSoup(html, "html.parser")
	resultCount = soup.findAll("span", {"class":"resultCount"})

	numItems = int(resultCount[0].strong.next_sibling.next_sibling.next_sibling.next_sibling.get_text())
	print("Search returned "+str(numItems)+" results")
	numItems += 1
	for x in range(2,numItems):
		get_jobs(jobs_url)
		jobs_url = re.sub('page=\d*','page=' + str(x), jobs_url)


	'''
	html = urllib.request.urlopen(jobs_url)
	soup = BeautifulSoup(html, "html.parser")


	pagesContainer = soup.findAll(href=re.compile("milwaukeejobs.com/jobs.asp\?pagemode=13"))
	print(len(pagesContainer))
	
	get_jobs(jobs_url)

	f = open("atags.html", 'w')
	for tag in pagesContainer:
		href = htmlmodule.unescape(tag["href"])
		#href.replace(u'\xb0', 'deg')
		#href = href.encode('utf-8', 'replace') 
		href = href.replace('\xb0','&deg')
		#href = href.decode('ascii', 'ignore')
		#href = href.replace('ree_id=','')
		print(type(href))
		print(href)
		
		f.write(href)
		f.write("\n\n")
		get_jobs(href)
			
	f.close()
	'''
if __name__ == '__main__':
	main()


