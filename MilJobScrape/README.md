###README

#Milwaukee Jobs Web Scraper

##Getting Started

This is a simple command line webscrapper for determining the word frequency used in job postings at https://milwaukeejobs.com. After the prerequisites are fulfilled you can run this progam in your shell. 	

###Usage


From Bash Shell, make sure you have read/write priviledges for Webscrapper directory
```
cd <path_to_dir>/Webscrapper
sudo chmod -R ugo+rw .
```

**Note:** all .txt files excluding "stopwords.txt" will be deleted after every run of word_freq.py

If you would like to ommit any words from the frequency counting, add the word on separate lines to "stopwords.txt". 

Run the word_freq.py program from the command line
```
python word_freq.py
```

Enter your search terms when prompted. 

Enter the top number of words to calculate. 

Output will be displayed to screen based on input. 

Entire word frequency dictionary will be posted to "data.json" file. 

###Prerequisites

```
Python 3.X
BeautifulSoup4
Command Line Knowledge
Read and Write priviledges for cwd
```
