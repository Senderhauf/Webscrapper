from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import re
import html as htmlmodule
import sys
from time import sleep

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
	html_text = re.sub('.*countered\swith\sevidence\sfrom\sa\sbetter\sone', '', html_text, flags=(re.IGNORECASE|re.DOTALL))
	html_text = re.sub('about\sblog\sabout\sadvertise.*', '', html_text, flags=(re.IGNORECASE|re.DOTALL))

	return html_text

def post_to_file(my_url, filename):
	f = open(filename, "w+")
	req = urllib.request.Request(my_url, headers={'User-Agent':'EnigmaticMustard'})
	html = urllib.request.urlopen(req)
	f.write(text_from_html(html))


# Print iterations progress
# source: https://gist.github.com/aubricus/print_progress.py
# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()


def get_comments(url):
	req = urllib.request.Request(my_url, headers={'User-Agent':'EnigmaticMustard'})
	html = urllib.request.urlopen(req)
	soup = BeautifulSoup(html, "html.parser")

	postsContainer = soup.findAll("div", {"class":"entry unvoted"})
	numPosts = len(postsContainer)

	printProgressBar(0, numItems, prefix = 'Progress:', suffix = 'Complete', length = 50)
	x = 0
	for post in postsContainer:
		postDetail = post.div.p.a
		filename = postDetail.get_text()
		filename = filename.replace('/', '')
		filename = filename.replace(' ', '_')
		filename += '.txt'
		printProgressBar(x , numItems, prefix = 'Progress:', suffix = 'Complete', length = 50)
		x += 1
		post_to_file('https://www.reddit.com' + postDetail["href"], filename)

def main():
	subreddit = input("Enter Subreddit: ")
	subreddit.strip()
	url = 'https://www.reddit.com/r/'+subreddit+'/top/?sort=top&t=month'
	get_comments(url)
	print()	

if __name__ == '__main__':
	post_to_file('https://www.reddit.com/r/NeutralPolitics/comments/89vyu1/if_our_schools_were_better_funded_would_student/', 'test.txt')